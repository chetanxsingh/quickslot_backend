from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="display_name", read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "name")

