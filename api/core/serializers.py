from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "email", "first_name", "last_name")

    def create(self, validated_data):
        # create_user garante o hash da senha
        return User.objects.create_user(**validated_data)
