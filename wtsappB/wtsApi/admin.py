from django.contrib import admin
from .models import usersData,messages,chatBox,imageBox,fileBox
# Register your models here.

admin.site.register(usersData)
admin.site.register(messages)
admin.site.register(chatBox)
admin.site.register(imageBox)
admin.site.register(fileBox)