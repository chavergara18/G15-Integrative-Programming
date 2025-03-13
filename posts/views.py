from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from .factories import PostFactory
from .singleton import PostConfigManager  
from .pagination import PostPagination 
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

User = get_user_model()


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/auth/google/callback/"
    client_class = OAuth2Client


class GoogleAuthVerifyView(APIView):
    permission_classes = [permissions.AllowAny]  

    def post(self, request):
        token = request.data.get("id_token")  

        if not token:
            return Response({"error": "ID Token is required"}, status=400)

        try:
            decoded_token = id_token.verify_oauth2_token(token, requests.Request())

            if "sub" not in decoded_token:
                return Response({"error": "Invalid token"}, status=400)

            email = decoded_token.get("email")
            user, created = User.objects.get_or_create(email=email)
            drf_token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "token": drf_token.key,
                "email": email,
                "created": created
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class NewsFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostPagination  

    def get_queryset(self):
        return (
            Post.objects
            .select_related("author")  # Load author efficiently
            .prefetch_related(Prefetch("comments"), Prefetch("likes"))  # Optimize related data
            .order_by("-created_at")  # Newest posts first
        )


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = PostFactory.create_post(author=self.request.user, **serializer.validated_data)
        serializer.save(instance=post)


class PostRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        post = self.get_object()
        config_manager = PostConfigManager()

        if not config_manager.get_config().get("allow_editing", True):
            raise PermissionDenied("Editing is currently disabled.")

        if post.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this post.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this post.")
        super().perform_destroy(instance)


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"message": "You have already liked this post."}, status=400)

        return Response({"message": "Post liked successfully.", "post_id": post.id}, status=201)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        like = Like.objects.filter(user=request.user, post_id=post_id)
        if like.exists():
            like.delete()
            return Response({"message": "Post unliked successfully."}, status=200)

        return Response({"message": "You have not liked this post yet."}, status=400)


class CommentPostView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(user=self.request.user, post=post)  


class PostCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id)


class SingletonConfigView(APIView):
    """View to access Singleton instance settings"""
    permission_classes = [permissions.IsAuthenticated]  

    def get(self, request):
        singleton_instance = PostConfigManager()  
        return Response({"config": singleton_instance.settings})














