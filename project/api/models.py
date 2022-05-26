from django.db import models


class Message(models.Model):
    class Status(models.TextChoices):
        REW = '1', "review"
        BLO = '2', "blocked"
        COR = '3', "correct"

    text = models.CharField(max_length=1024, default='sample text', blank=True, verbose_name='текст сообщения')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.REW, blank=True, verbose_name='статус сообщения')


    class Meta:
        ordering = ['status']
    
    def __str__(self):
        return self.text


# Create your models here.
