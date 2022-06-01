from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from api.models import  Message
from api.serializers import  MessageSerializer, MessageConfirmationSerializer
from django.core.exceptions import ObjectDoesNotExist




class MessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []


    def send_message_to_kafka(self):
        pass


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        self.perform_create(serializer)

        self.send_message_to_kafka()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# -------------------------------------------------------------------------------------------WORKING WITHOUT JWT
# @swagger_auto_schema(method='POST', request_body=MessageConfirmationSerializer)
# @api_view(['POST'])
# def message_confirmation(request):

#     data = request.data
#     try:
#         message = Message.objects.get(id=data['message_id'])
#         if data['success']:
#             message.status = 'correct'
#             message.save()
#             return Response('message status set [correct]', status=status.HTTP_200_OK)
#         else:
#             message.status = 'blocked'
#             message.save()
#             return Response('message status set [blocked]', status=status.HTTP_200_OK)
#     except ObjectDoesNotExist:
#         return Response('Object with id={} does not exists.'.format(data['message_id']))
# --------------------------------------------------------------------------------------------WORKING WITHOUT JWT


class ConfirmationView(APIView):
    permissions_classes = [permissions.IsAuthenticated,]
    

    @swagger_auto_schema(method='POST', request_body=MessageConfirmationSerializer)
    @action(methods=['POST'], detail=False, url_path='message_confirmation', url_name='message_confirmation')
    def post(self, request):

        return Response(request.data)


# Create your views here.