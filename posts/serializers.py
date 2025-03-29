from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Like, Comment, UserProfile

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile, including role-based access control"""
    class Meta:
        model = UserProfile
        fields = ["role"]

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model, includes role from UserProfile"""
    role = serializers.CharField(source="userprofile.role", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role"]

class PostSerializer(serializers.ModelSerializer):
    """Serializer for Posts, including privacy settings"""
    title = serializers.CharField(max_length=255, required=True)
    content = serializers.CharField(required=True)
    privacy = serializers.ChoiceField(choices=[("public", "Public"), ("private", "Private")], required=True)
    
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)  # ✅ Show author details

    class Meta:
        model = Post
        fields = "__all__"

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate_privacy(self, value):
        """Ensure privacy is set correctly."""
        if value not in ["public", "private"]:
            raise serializers.ValidationError("Invalid privacy setting.")
        return value

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    
    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]

    def validate(self, data):
        """Prevent users from liking posts they don't have access to."""
        post = data["post"]
        user = self.context["request"].user

        if not post.is_visible_to(user):
            raise serializers.ValidationError("You do not have permission to like this post.")
        
        return data

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ["id", "user", "post", "content", "created_at"]
        read_only_fields = ["user"]  

    def validate(self, data):
        """Prevent users from commenting on posts they don’t have access to."""
        post = data["post"]
        user = self.context["request"].user

        if not post.is_visible_to(user):
            raise serializers.ValidationError("You do not have permission to comment on this post.")
        
        return data




