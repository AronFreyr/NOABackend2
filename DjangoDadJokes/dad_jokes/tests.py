import requests
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

# Get the EXTERNAL_API_URL from the settings
from django.conf import settings
from .utils import get_dad_joke_from_api, DadJoke as DadJokeObj
from .models import DadJoke

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

class DadJokeCrudOperations(APITestCase):
    """
    Test case for CRUD operations on Dad Jokes.
    """

    def setUp(self):
        self.dad_joke = DadJokeObj(joke="This is a test joke", site_id="test123")
        self.dad_joke_url = '/dad-jokes/dad-jokes/'
        # save the joke to the database
        self.test_joke = DadJoke.objects.create(joke=self.dad_joke.joke, site_id=self.dad_joke.site_id)


    def test_list_jokes(self):
        response = self.client.get(self.dad_joke_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_joke(self):
        data = {"joke": "Another test joke", "site_id": "test456"}
        response = self.client.post(self.dad_joke_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['joke'], data['joke'])

    def test_retrieve_joke(self):
        response = self.client.get(f'{self.dad_joke_url}{self.test_joke.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['joke'], self.dad_joke.joke)

    def test_update_joke(self):
        data = {"joke": "Updated joke", "site_id": self.dad_joke.site_id}
        response = self.client.put(f'{self.dad_joke_url}{self.test_joke.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['joke'], data['joke'])

    def test_delete_joke(self):
        response = self.client.delete(f'{self.dad_joke_url}{self.test_joke.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DadJoke.objects.filter(id=self.test_joke.id).exists())