# Generated by Django 4.0.4 on 2022-06-30 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='usersContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=250)),
                ('phone_number', models.CharField(max_length=250)),
                ('user_id', models.IntegerField()),
                ('image_url', models.CharField(max_length=250)),
                ('messages', models.TextField()),
            ],
            options={
                'ordering': ('username',),
            },
        ),
    ]