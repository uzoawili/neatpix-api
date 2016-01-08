from django.test import TestCase
from django.contrib.auth.models import User
from webapp.models import SocialProfile, Photo


class ModelsTestCase(TestCase):
    """
    Testcase for the Utility functions .
    """
    fixtures = ['sample_data.json']

    def setUp(self):
        """
        operations to be done before every test
        """
        self.user = User.objects.get(id=7)

    def test_social_profile_model(self):
        social_profile = self.user.social_profile
        self.assertEquals(str(social_profile), '1:10207225470607962')

    def test_photo_model_can_be_serialized(self):
        photo = Photo.objects.get(public_id='e3w3wl9m21rz')
        self.assertEquals(str(photo), '<Photo: Nosa the boss-e3w3wl9m21rz')
        ser_photo = photo.serialize()
        self.assertEquals(ser_photo.get('public_id'), 'e3w3wl9m21rz')
        self.assertEquals(ser_photo.get('filename'), 'e3w3wl9m21rz.jpg')
        self.assertEquals(ser_photo.get('username'), 'AwiliUzo')
        self.assertEquals(ser_photo.get('caption'), 'Nosa the boss')
