# Generated by Django 4.0.4 on 2022-07-02 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wtsApi', '0004_alter_filebox_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='filebox',
            name='name',
            field=models.CharField(default='', max_length=150),
        ),
    ]
