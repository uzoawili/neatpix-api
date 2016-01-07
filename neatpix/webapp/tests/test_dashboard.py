from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class IndexTestCase(TestCase):
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

    def test_user_can_access_the_dashboard_view(self):
        """
        Tests that a get request to the dashboard
        view returns and renders successfully.
        """
        response = self.client.get(
            reverse('webapp:dashboard')
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('Logged in as', response.content)
