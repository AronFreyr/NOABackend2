from .models import DadJoke
from .serializers import DadJokeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_dad_joke_from_api

class FetchAndStoreDadJokeFromAPI(APIView):
    """
    API view to fetch a dad joke from external API and store it in the database.
    """
    def post(self, request):
        try:
            joke_data = get_dad_joke_from_api()
            dad_joke = DadJoke.objects.create(
                joke=joke_data.joke,
                site_id=joke_data.site_id
            )
            serializer = DadJokeSerializer(dad_joke)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DadJokeList(APIView):
    """
    API view to list all dad jokes.
    """
    def get(self, request):
        """Gets every dad joke from the database."""
        queryset = DadJoke.objects.all()
        serializer = DadJokeSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Creates a new dad joke and stores it in the database."""
        serializer = DadJokeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)