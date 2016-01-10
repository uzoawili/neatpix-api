from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.files import File

import PIL
from PIL import Image
from mock import patch, MagicMock

from webapp.forms import PhotoForm


class DashboardTestCase(TestCase):
    """
    Testcase for the Dashboard View .
    """
    fixtures = ['sample_data.json']

    def setUp(self):
        """
        operations to be done before every test
        """
        # create a test client:
        self.client = Client()
        self.user_credentials = {
            'id': '10207225470607962',
            'first_name': 'Awili',
            'last_name': 'Uzo',
            'email': 'awilo@ymail.com',
            'photo': 'http://graph.facebook.com/sample_image',
            'picture': {
                'data': {
                    'url': 'http://graph.facebook.com/sample_image',
                    'is_silouhette': True,
                }
            }
        }
        # login a user:
        self.client.post(
            reverse('webapp:facebook_auth'),
            self.user_credentials
        )
        self.mock_photo = MagicMock()
        self.mock_photo.serialize = MagicMock(return_value="<photo>")

    def test_logged_in_user_can_access_the_dashboard_view(self):
        """
        Tests that a get request to the dashboard
        view returns and renders successfully.
        """
        response = self.client.get(
            reverse('webapp:dashboard')
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('Logged in as', response.content)
        self.assertIn('photo_effects', response.context)

    def test_unauthenticated_user_is_redirected_to_index_auth_view(self):
        """
        Tests that a request to the dashboard by an unauthenticated
        user is redirected to the index/auth view.
        """
        response = Client().get(
            reverse('webapp:dashboard')
        )
        self.assertEquals(response.status_code, 302)

    def test_user_can_view_their_uploaded_photos(self):
        """
        Tests that a user sees a list of their uploaded
        photos as loaded by the photoList component.
        """
        response = self.client.get(
            reverse('webapp:photos')
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('success', response.content)
        self.assertIn('data', response.content)

    @patch(
        'webapp.forms.PhotoForm.save',
        return_value=MagicMock(
            serialize=MagicMock(return_value="<serialized_photo>")
        )
    )
    @patch('PIL.Image')
    def test_user_can_upload_photo(self, mock_form_save, mock_image):
        """
        Tests that an authenticated user can upload a
        photo to the server from their file system.
        """
        mock_uploaded_file = MagicMock(
            spec=File,
            name="mock_image_file.jpg",
            content_type='image/jpeg',
            size=84625
        )

        response = self.client.post(
            reverse('webapp:photo_upload'),
            {'image': mock_uploaded_file}
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('success', response.content)
        self.assertIn('photoData', response.content)
        self.assertTrue(PhotoForm.save.called)

    @patch(
        'webapp.forms.PhotoForm.save',
        return_value=MagicMock(
            serialize=MagicMock(return_value="<serialized_photo>")
        )
    )
    @patch('PIL.Image')
    def test_cannot_upload_invalid_photo(self, mock_form_save, mock_image):
        """
        Tests that an authenticated user cannot a upload
        an invalid photo file or data to the server.
        """
        response = self.client.post(
            reverse('webapp:photo_upload'),
            {'image': ''}
        )
        self.assertEquals(response.status_code, 403)
        self.assertIn('invalid', response.content)

    @patch.object(Image, "open")
    def test_fetching_photo_without_effects(self, mock_image_open):
        """
        Tests that photos can be fetched without
        any effects.
        """
        response = self.client.get(
            reverse(
                'webapp:photo_service',
                kwargs={
                    'username': 'AwiliUzo',
                    'filename': 'e3w3wl9m21rz.jpg',
                }
            )
        )
        self.assertEquals(response.status_code, 200)

    @patch.object(Image, "open")
    def test_photo_can_be_downloaded(self, mock_image_open):
        """
        Tests that photos can be downloaded
        """
        response = self.client.get(
            reverse(
                'webapp:photo_service',
                kwargs={
                    'username': 'AwiliUzo',
                    'filename': 'e3w3wl9m21rz.jpg',
                }
            ) + "?download=true"
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn(response['Content-Disposition'],
                      'attachment; filename="e3w3wl9m21rz.jpg"')

    def test_user_can_update_photo_caption(self):
        """
        Tests that user can update the default
        caption for photos.
        """
        response = self.client.post(
            reverse(
                'webapp:photo_update_delete',
                kwargs={'public_id': 'e3w3wl9m21rz'}
            ),
            {'caption': 'Caribbean Chilling'}
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('success', response.content)
        self.assertIn('photoData', response.content)
        self.assertIn('Caribbean Chilling', response.content)

    def test_user_can_update_effects_caption(self):
        """
        Tests that user can update the persistent
        effects for a photo.
        """
        response = self.client.post(
            reverse(
                'webapp:photo_update_delete',
                kwargs={'public_id': 'e3w3wl9m21rz'}
            ),
            {'effects': 'charcoal,blur'}
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('success', response.content)
        self.assertIn('photoData', response.content)
        self.assertIn('charcoal,blur', response.content)

    @patch("os.path.exists", return_value=True)
    @patch("os.remove")
    def test_user_can_delete_photo(self, mock_path_exists, mock_os_remove):
        """
        Tests that user can delete uploaded photos.
        """
        response = self.client.delete(
            reverse(
                'webapp:photo_update_delete',
                kwargs={'public_id': 'e3w3wl9m21rz'}
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('success', response.content)
