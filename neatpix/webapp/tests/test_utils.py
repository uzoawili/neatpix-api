from django.test import TestCase
from webapp.utils import genuid, get_photo_upload_path
from webapp.models import Photo


class UtilsTestCase(TestCase):
    """
    Testcase for the Utility functions .
    """
    fixtures = ['sample_data.json']

    def setUp(self):
        """
        operations to be done before every test
        """
        pass

    def test_uid_generation_for_photo_public_ids(self):
        """
        Tests that unique ids can be generated
        fpr use as photo public_ids.
        """
        public_id = genuid()
        self.assertFalse(Photo.objects.filter(public_id=public_id).exists())

    def test_get_photo_upload_path(self):
        """
        Tests that an upload path (relative to MEDIA_ROOT)
        including the filename for the Photo file
        can be obtained.
        """

        instance = Photo.objects.get(public_id='e3w3wl9m21rz')
        filename = 'sample_file_name.jpg'
        path = get_photo_upload_path(instance, filename)

        self.assertEquals(path, 'photos/AwiliUzo_7/e3w3wl9m21rz.jpg')
