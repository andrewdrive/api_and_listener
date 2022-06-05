from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .models import Message
from .serializers import (MessageSerializer,
                          MessageConfirmationSerializer,
                          CustomTokenObtainSerializer)
from .kafka_producer import on_send_error, on_send_success, producer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView


class MessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def send_message_to_kafka(data):
        producer.send('message_topic', data).add_callback(on_send_success).add_errback(on_send_error)

    def perform_create(self, serializer):
        return serializer.save().id

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message_id = self.perform_create(serializer)
        user_id = serializer.validated_data['user_id'].id
        text = serializer.validated_data['text']
        data = {'user_id': user_id, 'message_id': message_id, 'text': text}
        self.send_message_to_kafka(data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ConfirmationView(APIView):
    permissions_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = MessageConfirmationSerializer

    @swagger_auto_schema(method='POST', request_body=MessageConfirmationSerializer)
    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
    def post(self, request):
        data = {}
        serializer = MessageConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        try:
            message = Message.objects.get(id=data['message_id'])
            if data['success']:
                message.status = 'correct'
                message.save()
                return Response('message status set [correct]', status=status.HTTP_200_OK)
            else:
                message.status = 'blocked'
                message.save()
                return Response('message status set [blocked]', status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response('Object with id={} does not exists.'.format(data['message_id']))


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer

