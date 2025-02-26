from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    content = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = '__all__'

    
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value
