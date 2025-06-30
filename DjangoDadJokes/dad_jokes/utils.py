import requests
from django.conf import settings
from dataclasses import dataclass

@dataclass
class DadJoke:
    """
    Represents a dad joke.
    """
    joke: str
    site_id: str

    def __str__(self):
        return self.joke


def get_dad_joke_from_api() -> DadJoke:
    """
    Fetches a random dad joke from the external API.
    Returns:
        DadJoke: A dataclass instance containing the joke and its ID, for easier handling.
    """

    api_url = settings.EXTERNAL_API_URL
    headers = {'Accept': 'application/json'}

    response = requests.get(api_url, headers=headers, timeout=10)

    if response.status_code == 200:
        dad_joke = DadJoke(joke=response.json().get('joke'), site_id=response.json().get('id'))
        return dad_joke
    else:
        raise Exception(f"Failed to fetch dad joke. Status code: {response.status_code}, Response: {response.text}")
