from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):

    model = Message
    list_display = ['id', 'text', 'status']
    ordering = ['status']
   

admin.site.register(Message, MessageAdmin)


# Register your models here.
