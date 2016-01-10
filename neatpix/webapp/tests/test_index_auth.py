from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class IndexTestCase(TestCase):
    """
    Testcase for the Index View .
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

    def test_user_can_access_the_index_view(self):
        """
        Tests that a get request to the index
        view returns and renders successfully.
        """
        response = self.client.get(
            reverse('webapp:index')
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('Log in with Facebook', response.content)

    def test_index_view_redirects_to_dashboard_for_authenticated_user(self):
        """
        Tests that a get request to the index redirects to
        dashboard for an already authenticated user.
        """
        # log a user in:
        self.client.post(
            reverse('webapp:facebook_auth'),
            self.user_credentials
        )
        response = self.client.get(
            reverse('webapp:index')
        )
        self.assertEquals(response.status_code, 302)

    def test_new_user_can_authenticate_with_facebook(self):
        """
        Tests that a new user can successfully
        authenticate with Facebook.
        """
        response = self.client.post(
            reverse('webapp:facebook_auth'),
            {
                'id': '2178192107389',
                'first_name': 'Lagbaja',
                'last_name': 'Somebody',
                'email': 'awilliballz@ymail.com',
                'photo': 'http://graph.facebook.com/sample_image',
                'picture': {
                    'data': {
                        'url': 'http://graph.facebook.com/sample_image',
                        'is_silouhette': False,
                    }
                }
            }
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('success', response.content)

    def test_existing_user_can_authenticate_with_facebook(self):
        """
        Tests that an existing user can successfully
        authenticate with Facebook.
        """
        response = self.client.post(
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
        self.assertEquals(response.status_code, 200)
        self.assertIn('success', response.content)

    def test_invalid_facebook_user_data_returns_error(self):
        """
        Tests that the appropriate error status is
        returned for invalid Facebook credentials.
        """
        response = self.client.post(
            reverse('webapp:facebook_auth'),
            {
                'first_name': 'Awili',
                'last_name': 'Uzo',
                'email': 'awilo@ymail.com',
            }
        )
        self.assertEquals(response.status_code, 403)
        self.assertIn('error', response.content)

    def test_auth_logout(self):
        """
        Tests that a user can logout of the session
        and is then redirected to the home.
        """
        # log a user in:
        self.client.post(
            reverse('webapp:facebook_auth'),
            self.user_credentials
        )
        # log user out and check response:
        response = self.client.get(
            reverse('webapp:logout')
        )
        self.assertEquals(response.status_code, 302)
