import requests
from django.test import TestCase

# Get the EXTERNAL_API_URL from the settings
from django.conf import settings
from .utils import get_dad_joke_from_api, DadJoke as DadJokeObj

class DadJokesFromAPI(TestCase):
    """
    Test case for the Dad Jokes API.
    """

    def setUp(self):
        self.api_url: str = settings.EXTERNAL_API_URL

    def test_get_joke_from_api(self):
        """
        Test that we can retrieve a joke from the API.
        """
        headers = {'Accept': 'application/json'}
        resp = requests.get(self.api_url, headers=headers, timeout=1)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('joke', data)
        self.assertIn('id', data)

    def test_get_joke_util(self):
        """Get a joke using the utility function."""
        dad_joke = get_dad_joke_from_api()
        self.assertIsInstance(dad_joke.joke, str)
        self.assertIsInstance(dad_joke.site_id, str)
        self.assertGreater(len(dad_joke.joke), 0)