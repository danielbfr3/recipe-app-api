from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User object"""

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "password",
            "name",
        )  # campos que quero disponibilizar para a API ler e escrever

        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

