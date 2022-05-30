from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from api.models import  Message
from api.serializers import  MessageSerializer





class MessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


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


    # def create(self, request, *args, **kwargs):
    #     text = 'hello'
    #     response = {'response', text}
    #     print(text)
    #     return Response(response)
        


# Create your views here.
