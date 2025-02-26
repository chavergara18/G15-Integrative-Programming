from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from .factories import PostFactory
from .singleton import PostConfigManager  # Ensure correct import

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = PostFactory.create_post(author=self.request.user, **serializer.validated_data)
        serializer.instance = post

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
        instance.delete()

class SingletonConfigView(APIView):
    """View to access Singleton instance settings"""
    def get(self, request):
        singleton_instance = PostConfigManager()  # Get Singleton instance
        return Response({"config": singleton_instance.settings})







