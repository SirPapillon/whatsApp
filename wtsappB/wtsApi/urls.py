from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    # path("choose/chat_id=<chatid>&sender_id=<senderid>&user_id=<userid>", views.getMessages),
    path("login", views.login),
    path("getMessages/chat_id=<chat_id>", views.getMessages),
    path("getUserByPhoneNumber/", views.getUsersByPhoneNumber),
    path("sendMessage/", views.sendMessage),
    path("startNewChat/", views.startNewChat),
    path("getPvOtherSide/user_id=<user_id>&chat_id=<chat_id>", views.pvOtherSide),
    path("downloadImage/", views.downloadImage),
    path("getChats/user_id=<user_id>", views.getUserChats),
    path("getChatInfos/chat_id=<chat_id>", views.getChatInfos),
    path("getUserInfos/user_id=<user_id>", views.getUserInfos),
    path("sendImage/", views.sendImage),
    path("getImage/image_id=<image_id>", views.ImageUrlByImageId),
    path("checkUserByPhone/phone_number=<phone_number>", views.checkUserByPhone),
    path("createGroup/", views.createGroup),
    path("groupInCommon/chat_id=<chat_id>", views.groupsInCommon),
    path("sendFile/", views.uploadFile),
    path("changeGroupImage/", views.changeGroupImage),
    path("changeGroupName/", views.changeGroupName),
    path("addParticipants/", views.addParticipants),
    path("changeGroupDescription/", views.changeGroupDescription),

    path("exitGroup/", views.exitGroup),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)