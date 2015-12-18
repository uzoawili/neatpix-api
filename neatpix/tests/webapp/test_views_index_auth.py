from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class IndexTestCase(TestCase):
    """
    Testcase for the Index View .
    """
    def setUp(self):
        """ operations to be done before every test
        """
        # create a test client:
        self.client = Client()

    def test_get_index_view_returns_success(self):
        """
        Tests that a get request to the index 
        view returns and renders successfully.
        """
        response = self.client.get(
            reverse('index')
        )
        self.assertEquals(response.status_code, 200)