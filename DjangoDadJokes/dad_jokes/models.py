"""Models for the dad jokes app."""
from django.db import models

class DadJoke(models.Model):
    """Model that represents a dad joke as gotten from https://icanhazdadjoke.com/api"""

    site_id = models.CharField(max_length=255, unique=True)  # ID gotten from the API
    joke = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.joke}"
