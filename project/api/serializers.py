from rest_framework import serializers
from api.models import Message


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
        