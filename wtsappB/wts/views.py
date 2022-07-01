from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response,responses
from .models import usersContent
from .serializers import usersContentSerializer

@api_view(["GET"])
def users(requests):
    identity=usersContent.objects.all()
    usernames_ser=usersContentSerializer(identity,many=True)
    return Response(usernames_ser.data)

