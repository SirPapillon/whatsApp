from rest_framework import serializers
from .models import usersContent

class usersContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=usersContent
        fields="__all__"