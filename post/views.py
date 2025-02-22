from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from .permissions import IsPostAuthor
from .models import Post
from .serializers import PostSerializer

# Singleton Pattern for a Post Manager
class PostManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PostManager, cls).__new__(cls)
        return cls._instance

    def create_post(self, data):
        return Post.objects.create(**data)

post_manager = PostManager()

# Factory Pattern for User Creation
class UserFactory:
    @staticmethod
    def create_user(username, password):
        if User.objects.filter(username=username).exists():
            return None
        return User.objects.create_user(username=username, password=password)

# User Registration View
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    user = UserFactory.create_user(data['username'], data['password'])
    if user:
        return Response({"message": "User registered successfully"})
    return Response({"error": "Username already exists"}, status=400)

# User Authentication
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    data = request.data
    user = authenticate(username=data['username'], password=data['password'])
    if user is not None:
        return Response({"message": "Authentication successful!"})
    else:
        return Response({"error": "Invalid credentials"}, status=401)

# API View for listing and creating posts
class PostListCreateView(generics.ListCreateAPIView):  
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# API View for Post Detail with permission checks
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        self.check_object_permissions(request, post)
        return Response({"content": post.content})

# Protected API View with Token Authentication
class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authenticated!"})
















