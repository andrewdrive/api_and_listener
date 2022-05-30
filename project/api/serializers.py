from email.policy import default
from rest_framework import serializers
from api.models import Message


class MessageSerializer(serializers.ModelSerializer):
    #status = serializers.CharField(max_length=10, default='sample text', allow_blank=True)

    class Meta:
        model = Message
        fields = ['user_id', 'text']


class MessageConfirmationSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    success = serializers.BooleanField()

    def validate_message_id(self, value):
        if Message.objects.filter(id=value).exists():
            return value
        else:
            raise serializers.ValidationError('There is no such message with {} id'.format(value))
