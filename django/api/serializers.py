from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "code", "host", "created_at")


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields: ("id", "code", "host")
