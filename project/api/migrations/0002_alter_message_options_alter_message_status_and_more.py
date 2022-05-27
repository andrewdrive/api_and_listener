# Generated by Django 4.0.4 on 2022-05-27 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['status']},
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(blank=True, choices=[('review', 'Review'), ('blocked', 'Blocked'), ('correct', 'Correct')], default='review', max_length=10, verbose_name='статус сообщения'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.CharField(blank=True, default='sample text', max_length=1024, verbose_name='текст сообщения'),
        ),
    ]
