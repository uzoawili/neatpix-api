import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import HttpResponse

from PIL import Image

from models import Photo
from forms import FacebookAuthForm, PhotoForm
from decorators import json_response
from effects import photo_effects, thumbnail

from neatpix.settings.base import MAX_UPLOAD_SIZE


class LoginRequiredMixin(object):
    """
    View mixin which requires that the user is authenticated.
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class JsonResponseMixin(object):
    """
    View mixin which requires that the user is authenticated.
    """
    @method_decorator(json_response)
    def dispatch(self, request, *args, **kwargs):
        return super(JsonResponseMixin, self).dispatch(
            request, *args, **kwargs)


class IndexView(View):
    """
    The index/login view.
    """
    def get(self, request, *args, **kwargs):
        """
        Renders the index/home view
        """
        # redirect to dashboard if user is already signed in:
        if request.user.is_authenticated():
            return redirect(reverse('webapp:dashboard'))
        # show index view:
        context = {}
        context.update(csrf(self.request))
        return render(self.request, 'webapp/index.html', context)


class FacebookAuthView(JsonResponseMixin, View):
    """
    Logs a user in with their facebook account.
    """
    def post(self, request, *args, **kwargs):
        """
        Logs a user out and redirects to the index view.
        """
        auth_form = FacebookAuthForm(request.POST)
        if auth_form.is_valid():
            # get or create the user:
            user = auth_form.save()
            if user:
                profile = user.social_profile
                profile.extra_data = json.dumps(request.POST)
                profile.save()
                # log the user in:
                login(request, user)
                # return success response:
                return {
                    'status': 'success',
                    'status_code': 200,
                    'loginRedirectURL': reverse('webapp:dashboard'),
                }
        # return error response
        return {'status': 'error', 'status_code': 403, }


class LogoutView(LoginRequiredMixin, View):
    """
    Logs the user out.
    """
    def get(self, request, *args, **kwargs):
        """
        Logs a user out and redirects to the index view.
        """
        logout(request)
        return redirect(reverse('webapp:index'))


class DashboardView(LoginRequiredMixin, View):
    """
    Represents the signed in users' dashboard/workspace view.
    """
    def get(self, request, *args, **kwargs):
        """
        Renders the dashboard view.
        """
        # show index view:
        context = {
            'photo_effects': photo_effects,
        }
        context.update(csrf(self.request))
        return render(self.request, 'webapp/dashboard.html', context)


class PhotosListView(JsonResponseMixin, LoginRequiredMixin, View):
    """
    View to fetch the list of photos.
    """
    def get(self, request, *args, **kwargs):
        """
        Returns a JSON list of photos uploaded
        by the current user.
        """
        photos = Photo.objects.filter(user=request.user)\
                              .order_by('date_created')\
                              .all()
        photos = [photo.serialize() for photo in photos]
        return {
            'status': 'success',
            'status_code': 200,
            'data': photos,
        }


class PhotoUploadView(JsonResponseMixin, LoginRequiredMixin, View):
    """
    View to handle photo uploads.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles the upload of photos and returns
        a JSON serialization of the uploaded photo.
        """
        photoForm = PhotoForm(request.POST, request.FILES)

        if photoForm.is_valid():
            # check that the file size is valid:
            image_file_size = photoForm.files['image'].size
            if image_file_size <= MAX_UPLOAD_SIZE:
                # save the photo and image file:
                photo = photoForm.save(commit=False)
                # set the default caption and user:
                photo.caption = photo.image.name
                photo.user = request.user
                photo.save()
                # return the serialized photo:
                return {
                    'status': 'success',
                    'status_code': 200,
                    'photoData': photo.serialize(),
                }

        # return error response
        return {'status': 'invalid', 'status_code': 403, }


class PhotoUpdateDeleteView(JsonResponseMixin, LoginRequiredMixin, View):
    """
    View to handle changes to photos such as updating the
    applied effects, the caption or deleting it altogethter.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles the updating of photos and returns
        a JSON serialization of the updated photo.
        Note, this view cannot update the associated
        image file.
        """
        public_id = kwargs.get('public_id')
        photo = get_object_or_404(Photo, public_id=public_id)
        photoForm = PhotoForm(request.POST, instance=photo)
        if photoForm.is_valid():
            # save the photo:
            photo = photoForm.save()
            # return the serialized photo:
            return {
                'status': 'success',
                'status_code': 200,
                'photoData': photo.serialize(),
            }
        # return error response
        return {'status': 'invalid', 'status_code': 403, }

    def delete(self, request, *args, **kwargs):
        """
        Handles the deleting of photos.
        Note, the actual deletion of the associated
        image file is handled in the post_delete
        function defined in the models module.
        """
        public_id = kwargs.get('public_id')
        photo = get_object_or_404(Photo, public_id=public_id)
        photo.delete()
        # return error response
        return {'status': 'success', 'status_code': 200, }


class PhotoServiceView(View):
    """
    View to handle serving uploaded photos with
    effects (optional) applied.
    """
    content_type = "image/jpg"
    output_format = "JPEG"

    def get(self, request, *args, **kwargs):
        """
        Accepts a photo's public_id and optionally a list of
        effects to apply. Returns the image (FileResponse)
        with the applied effects.
        """
        # use the captured image specs from the url
        # to get the associated photo instance:
        filename = kwargs.get('filename')
        effects = kwargs.get('effects')
        public_id, ext = os.path.splitext(filename)
        photo = get_object_or_404(Photo, public_id=public_id)

        # get a pillow image instance for the photo:
        image = Image.open(photo.image.path)

        # convert image to thumbnail size if specified:
        if request.GET.get('thumbnail') == 'true':
            image = thumbnail(image)

        # apply any specified effects:
        if effects:
            effects = effects.split(',')
            for effect_name in effects:
                # get the matching effects:
                # import pdb; pdb.set_trace()
                matching_effects = [effect[1] for effect in photo_effects if effect[0] == effect_name]
                # apply the effect to the image:
                if len(matching_effects):
                    image = matching_effects[0](image)

        # save the image to a FileResponse instance:
        response = HttpResponse(content_type=self.content_type)
        image.save(response, self.output_format)

        # trigger download if specified:
        if request.GET.get('download') == 'true':
            response['Content-Disposition'] = 'attachment; filename="{}.jpg"'\
                                              .format(photo.public_id)
        return response
