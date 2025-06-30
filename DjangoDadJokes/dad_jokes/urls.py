from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


app_name = 'dad_jokes'

urlpatterns = [
    path('dad-jokes/', views.DadJokeList.as_view()),
    path('dad-jokes/<int:pk>/', views.DadJokeDetail.as_view()),
    path('fetch-dad-joke/', views.FetchAndStoreDadJokeFromAPI.as_view(), name='fetch_dad_joke_from_api'),
]