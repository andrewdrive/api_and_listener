from email.policy import default
from rest_framework import serializers
from api.models import Message


class MessageSerializer(serializers.ModelSerializer):
    #status = serializers.CharField(max_length=10, default='sample text', allow_blank=True)

    class Meta:
        model = Message
        fields = ['user_id', 'text']