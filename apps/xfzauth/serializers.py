from rest_framework import serializers
from .views import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'telephone', 'username', 'email', 'is_active', 'is_staff')
