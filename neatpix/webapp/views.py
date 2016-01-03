import json
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View

from models import Photo
from forms import FacebookAuthForm, PhotoForm
from decorators import json_response


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
                    'loginRedirectURL': reverse('webapp:dashboard'),
                }
        # return error response
        return {'status': 'error', }


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
        context = {}
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
        photos = Photo.objects.filter(user=request.user).all()
        photos = [photo.serialize() for photo in photos]
        return {
            'status': 'success',
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
            # save the photo and image file:
            photo = photoForm.save(commit=False)
            # set the default caption as the new filename:
            photo.caption = photo.image.name
            photo.user = request.user
            photo.save()
            # return the serialized photo:
            return {
                'status': 'success',
                'photoData': photo.serialize(),
            }
        # return error response
        return {'status': 'invalid', }
