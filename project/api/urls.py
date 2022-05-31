from django.db import router
from django.urls import path
from rest_framework import routers
from api import views


router = routers.SimpleRouter()
router.register('message', views.MessageViewSet)


urlpatterns = router.urls


urlpatterns += [
    #path('message_confirmation', views.message_confirmation),  -----------------WORKING WITHOUT JWT
    path('confirmation', views.ConfirmationView.as_view(), name='hello'),
]