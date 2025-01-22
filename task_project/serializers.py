from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    Class Meta:
        model = User
        fields = '__all__'