# task_api/serializers.py
from rest_framework import serializers
from .models import Task, Tag
from django.contrib.auth.models import User

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  # Nested UserSerializer
    tags = TagSerializer(many=True, read_only=True)  # Nested TagSerializer

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at', 'created_by', 'tags']

    # Custom validation for the title field
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    # Custom validation for the description if the task is completed
    def validate(self, data):
        if data['completed'] and not data.get('description'):
            raise serializers.ValidationError("Completed tasks must have a description.")
        return data

