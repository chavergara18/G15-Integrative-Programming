from rest_framework import serializers
from .models import Post, Like, Comment

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    content = serializers.CharField(required=True)

    # Add like and comment counts to the post response
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "post", "content", "created_at"]
        read_only_fields = ["user", "post"]  


