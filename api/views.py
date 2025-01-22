from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .Models import User 
from .serializer import UserSerializer

@api_view(['GET'])
def get_user(request):
    return Response(UserSerializer({'name': "Pedro", "age": "23"}))
