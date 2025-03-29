from google.oauth2 import id_token
from google.auth.transport import requests
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from .factories import PostFactory
from .singleton import PostConfigManager  
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100  


class NewsFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TaskPagination  

    def get_queryset(self):
        """Returns only public posts, sorted by creation date."""
        return (
            Post.objects
            .filter(privacy="public")
            .select_related("author")
            .prefetch_related(Prefetch("comments"), Prefetch("likes"))
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):
        """Caches paginated responses for improved performance."""
        page_number = request.GET.get("page", 1)
        cache_key = f"feed_page_{page_number}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)  # Cache for 5 minutes

        return response


User = get_user_model()


# ✅ Google OAuth Login
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/auth/google/callback/"
    client_class = OAuth2Client


# ✅ Post CRUD: Retrieve, Update, Delete
class PostRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Restricts access to only the post owner."""
        return Post.objects.filter(author=self.request.user)


# ✅ User Role Management
class UserRoleView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Only admins can assign roles

    def post(self, request):
        """Assigns a role to a user."""
        user_id = request.data.get("user_id")
        role = request.data.get("role")

        if role not in ["admin", "user", "guest"]:
            return Response({"error": "Invalid role."}, status=400)

        user = get_object_or_404(User, id=user_id)
        user.role = role  # Ensure 'role' field exists in User model
        user.save()

        return Response({"message": f"Role '{role}' assigned to {user.email}."})


# ✅ Privacy Settings for Posts
class PostPrivacyUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, post_id):
        """Allows the post owner to change privacy settings."""
        post = get_object_or_404(Post, id=post_id)

        if post.author != request.user:
            raise PermissionDenied("You can only update your own post's privacy settings.")

        new_privacy = request.data.get("privacy")
        if new_privacy not in ["public", "private"]:
            return Response({"error": "Invalid privacy setting."}, status=400)

        post.privacy = new_privacy
        post.save()

        return Response({"message": f"Post privacy updated to '{new_privacy}'."})


# ✅ Create & List Posts
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Uses PostFactory to create posts while enforcing business rules."""
        post = PostFactory.create_post(author=self.request.user, **serializer.validated_data)
        serializer.save(instance=post)
        cache.delete("feed_page_*")  # Invalidate cached feed pages


# ✅ Like a Post
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        """Allows users to like a post."""
        post = get_object_or_404(Post, id=post_id)
        Like.objects.get_or_create(user=request.user, post=post)
        cache.delete("feed_page_*")  # Invalidate cached feed pages
        return Response({"message": "Post liked!"})


# ✅ Unlike a Post
class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        """Allows users to unlike a post."""
        post = get_object_or_404(Post, id=post_id)
        Like.objects.filter(user=request.user, post=post).delete()
        cache.delete("feed_page_*")  # Invalidate cached feed pages
        return Response({"message": "Post unliked!"})


# ✅ Comment on a Post
class CommentPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        """Allows users to comment on a post."""
        post = get_object_or_404(Post, id=post_id)
        comment_text = request.data.get("comment")

        if not comment_text:
            return Response({"error": "Comment cannot be empty."}, status=400)

        Comment.objects.create(user=request.user, post=post, text=comment_text)
        cache.delete("feed_page_*")  # Invalidate cached feed pages
        return Response({"message": "Comment added!"})


# ✅ Retrieve Post Comments
class PostCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieve comments for a specific post."""
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id).select_related("user")


# ✅ Singleton Pattern for Post Configuration
class SingletonConfigView(APIView):
    """Uses Singleton to manage global post configurations."""

    def get(self, request):
        config = PostConfigManager()
        return Response({"message": "Singleton config retrieved!", "data": config.get_config()})

    def post(self, request):
        """Update singleton config settings."""
        new_config = request.data.get("config")
        config = PostConfigManager()
        config.update_config(new_config)
        return Response({"message": "Singleton config updated!", "data": config.get_config()})

















