from django.test import TestCase, Client
from django.core.urlresolvers import reverse


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
        # self.client.login(username='AwiliUzo', password='')
        self.client.post(
            reverse('webapp:facebook_auth'),
            {
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
        )

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

