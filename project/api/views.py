from rest_framework import viewsets, mixins
from rest_framework import permissions
from api.models import  Message
from api.serializers import  MessageSerializer


# mixins.ListModelMixin, viewsets.GenericViewSet
class MessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]




# Create your views here.
