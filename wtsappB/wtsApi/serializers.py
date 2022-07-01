from rest_framework import serializers
from .models import usersData,messages,chatBox,imageBox

class userDatasSerializers(serializers.ModelSerializer):
    class Meta:
        model=usersData
        fields="__all__"


class imageBoxSerializers(serializers.ModelSerializer):
    class Meta:
        model=imageBox
        fields="__all__"

class messageSerializers(serializers.ModelSerializer):
    class Meta:
        model=messages
        fields="__all__"

class chatBoxSerializers(serializers.ModelSerializer):
    class Meta:
        model=chatBox
        fields="__all__"

