# Generated by Django 4.0.4 on 2022-07-01 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wtsApi', '0002_filebox'),
    ]

    operations = [
        migrations.AddField(
            model_name='filebox',
            name='content_type',
            field=models.TextField(default='ds'),
        ),
    ]
