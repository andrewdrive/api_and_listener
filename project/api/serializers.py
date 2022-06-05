from rest_framework import serializers
from .models import Message
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['user_id', 'text']


class MessageConfirmationSerializer(serializers.ModelSerializer):
    message_id = serializers.IntegerField()
    success = serializers.BooleanField()

    class Meta:
        model = Message
        fields = ['message_id', 'success']


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = 'post_message_confirm'
        return token

        # Add custom claims
    