from django.db import models


class Message(models.Model):
    StatusType = models.TextChoices('StatusType', 'review blocked correct')
    text = models.CharField(max_length=1024, default='sample text', blank=True, verbose_name='текст сообщения')
    status = models.CharField(max_length=10, choices=StatusType.choices, default=StatusType.review, blank=True, verbose_name='статус сообщения')


    class Meta:
        ordering = ['status']
    
    def __str__(self):
        return self.text


# Create your models here.
