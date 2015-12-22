from django import forms
from django.contrib.auth.models import User

from models import SocialProfile


class FacebookAuthForm(forms.Form):
    """
    Form for validating and saving Facebook
    user authentication data. Returns the
    existing or created user.
    """

    id = forms.CharField(max_length=255)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    photo = forms.CharField(required=False)

    def save(self):
        """
        gets returns the social user with the form data.
        creates one if it does not already exists.
        """
        data = self.cleaned_data
        user = None
        try:
            # get associated user if it exists:
            social_id = data['id']
            social_profile = SocialProfile.objects.get(
                provider=SocialProfile.FACEBOOK,
                social_id=social_id,
            )
            user = social_profile.user

        except SocialProfile.DoesNotExist:

            # Create the user:
            user = User(
                username="{}{}".format(data['first_name'], data['last_name']),
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            user.save()

            # Create the user's social_profile:
            social_profile = SocialProfile(
                provider=SocialProfile.FACEBOOK,
                social_id=data['id'],
                photo=data['photo'],
                user=user
            )
            social_profile.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        return user
