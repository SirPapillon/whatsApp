import base64
import io
import datetime
import os
import re
from pathlib import Path
import PIL
from django.core.files.base import ContentFile
from django.http import QueryDict, HttpResponse, Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import usersData as modelInstance
from .models import chatBox as modelInstance_ch
from .models import imageBox as modelInstance_im
from .models import messages as messageInstance
from .serializers import userDatasSerializers, messageSerializers, chatBoxSerializers,imageBoxSerializers
import json
import random




def addMessage(chat_id,message,reply_to,user_id,message_type="message"):
    new_message_id=generate_new_message_id()
    dt = chatBoxSerializers(modelInstance_ch.objects.get(chat_id=chat_id)).data
    time_now=str(datetime.datetime.now())
    messages = json.loads(dt["messages"].replace("\'", "\""))
    message_template = {
        "sent_message": message,
        "time_created": time_now,
        "reply_to": reply_to,
        "message_id": new_message_id,
        "message_type":message_type,
        "user_id": user_id
    }
    messages.append(message_template)
    modelInstance_ch.objects.filter(chat_id=chat_id).update(messages=messages)

    message_box_template = {
        "chat_id": chat_id,
        "message_id": new_message_id,
        "sender_id": user_id,
        "time_created": time_now,
        "message": message
    }

    serializedMessageBox = messageSerializers(data=message_box_template)

    if serializedMessageBox.is_valid():
        serializedMessageBox.save()

def infoByUserid(user_id):
    info = userDatasSerializers(modelInstance.objects.get(user_id=user_id)).data
    return info

def ImageById(image_id):
    if image_id != -1:
        image = imageBoxSerializers(modelInstance_im.objects.get(image_id=image_id)).data["upload"]
    else:
        image = -1
    return image

def correctedPhoneNumber(messy_phone):
    if messy_phone.startswith("0"):
        return re.sub("^0", "+98", messy_phone).strip()
    elif messy_phone.startswith("+98"):
        return messy_phone
    return "+98"+messy_phone


def generate_group_chat_id():
    random_num = random.randint(2345678909800, 9923456789000)

    new_chat_id = modelInstance_ch.objects.filter(chat_id=random_num)

    while new_chat_id:
        random_num = random.randint(2345678909800, 9923456789000)
        if not modelInstance_ch.objects.filter(chat_id=random_num):
            break
    return random_num


def generate_group_image_id():
    random_num = random.randint(2345678909800, 9923456789000)

    new_image_id = modelInstance_im.objects.filter(image_id=random_num)

    while new_image_id:
        random_num = random.randint(2345678909800, 9923456789000)
        if not modelInstance_im.objects.filter(image=random_num):
            break
    return random_num

def generate_new_message_id():
    random_num = random.randint(2345678909800, 9923456789000)
    new_message_id = messageInstance.objects.filter(message_id=random_num)

    while new_message_id:
        random_num = random.randint(2345678909800, 9923456789000)
        if not messageInstance.objects.filter(message_id=random_num):
            break
    return random_num

def generate_user_id():
    random_num = random.randint(2345678909800, 9923456789000)

    new_chat_id = modelInstance.objects.filter(user_id=random_num)

    while new_chat_id:
        random_num = random.randint(2345678909800, 9923456789000)
        if not modelInstance.objects.filter(user_id=random_num):
            break
    return random_num


def getChatParticipants(chat_id):
    dt = chatBoxSerializers(modelInstance_ch.objects.get(chat_id=chat_id)).data
    participants=json.loads(dt["participants"].replace("\'","\""))
    return participants




@api_view(["POST"])
def sendImage(requests):
    form=modelInstance_im(requests.POST, requests.FILES)
    if form.is_valid():
        form.save()


@api_view(["POST"])
def sendMessage(requests):
    new_message_id=generate_new_message_id()

    data = requests.data
    chat_id = data["chat_id"]
    sent_message = data["sent_message"]
    time_created = data["time_created"]
    reply_to = data["reply_to"]
    user_id = data["user_id"]
    addMessage(chat_id,sent_message,reply_to,user_id)







    return Response({})




@api_view(["GET"])
def getUserInfos(requests,user_id):
    dt = userDatasSerializers(modelInstance.objects.get(user_id=user_id)).data
    del dt["user_chats_id"]
    dt.update({
        "profile_image_id":ImageById(dt["profile_image_id"])
    })

    return Response(dt)

@api_view(["GET"])
def getChatInfos(requests,chat_id):
    dt = chatBoxSerializers(modelInstance_ch.objects.get(chat_id=chat_id)).data

    if dt["chat_type"]=="person":
        return Response(dt)
    final_info={key:dt[key] for key in dt if key!="participants"}
    final_info["group_image_id"]=ImageById(final_info["group_image_id"])
    final_info["participants"]=[]
    participants=json.loads(dt["participants"].replace("\'","\""))
    for member in participants:
        user_data = userDatasSerializers(modelInstance.objects.get(user_id=int(member["user_id"]))).data
        profile_image_id=user_data["profile_image_id"]
        username=user_data["username"]
        phone_number=user_data["phone_number"]
        bio=user_data["bio"]
        image=ImageById(profile_image_id)
        member["profile_image_subdirectory"]=image
        member["username"]=username
        member["phone_number"]=phone_number
        member["bio"]=bio
        final_info["participants"].append(member)

    return Response(final_info)


@api_view(["GET"])
def getUserChats(requests, user_id):
    datas=[]
    dt = userDatasSerializers(modelInstance.objects.get(user_id=user_id)).data

    for chat_id in json.loads(dt["user_chats_id"].replace("\'", "\"")):

        chats=chatBoxSerializers(modelInstance_ch.objects.get(chat_id=int(chat_id["chat_id"]))).data

        if chats["chat_type"]=="group":
            chat_id["name"]=chats["group_name"]
            if chats["group_image_id"]!=-1:
                image_subdirectory = imageBoxSerializers(
                    modelInstance_im.objects.get(image_id=chats["group_image_id"])).data

                chat_id["profile_subdirectory"] = image_subdirectory
            else :
                chat_id["profile_subdirectory"]=-1


        else:
            tar_data=userDatasSerializers(modelInstance.objects.get(user_id=chat_id["participants_id"][1])).data
            chat_id["name"]=tar_data["phone_number"]
            if tar_data["profile_image_id"]!=-1:
                image_subdirectory = imageBoxSerializers(
                    modelInstance_im.objects.get(image_id=tar_data["profile_image_id"])).data

                chat_id["profile_subdirectory"]=image_subdirectory
            else:
                chat_id["profile_subdirectory"]=-1

        if len(json.loads(chats["messages"].replace("\'","\"")))>0:

            datas.append(
                {
                    "last_message":json.loads(chats["messages"].replace("\'","\""))[-1],
                    "chat_infos":chat_id

                }
            )
        else:
            datas.append(
                {
                    "last_message": {"sent_message":"group created" if chats["chat_type"]=="group" else "Hey there! I am using WhatsApp","time_created":"","reply_to":"","user_id":user_id},

                    "chat_infos": chat_id

                }
            )
    return Response(datas)
    # return Response(json.loads(dt["user_chats_id"].replace("\'", "\"")))


@api_view(["GET"])
def getMessages(requests, chat_id):
    allusersData = modelInstance_ch.objects.get(chat_id=chat_id)
    ser = chatBoxSerializers(allusersData)
    return Response(ser.data)


@api_view(["GET"])
def checkUserExist(requests, phone_number):
    allusersData = modelInstance_ch.objects.get(phone_number=phone_number)
    ser = chatBoxSerializers(allusersData)
    return Response(ser.data)


@api_view(["POST"])
def startNewChat(requests):
    datas = requests.data.dict()
    founded_chat_id = None

    res_id = datas['res_id']
    target_id = datas['target_id']
    #resorce datas
    dt = modelInstance.objects.get(user_id=res_id)
    allDatas = userDatasSerializers(dt).data
    res_chat_ids = allDatas
    f = json.loads(res_chat_ids['user_chats_id'].replace('\'', '\"'))

    #target datas
    dtt = modelInstance.objects.get(user_id=target_id)
    allDatasT = userDatasSerializers(dtt).data
    tar_chat_ids = allDatasT
    tf = json.loads(res_chat_ids['user_chats_id'].replace('\'', '\"'))

    for chat_c in f:
        print(chat_c)
        if  chat_c['chat_type'] == 'person':
            if len(chat_c['participants_id']) == 2 and (
                    str(res_id) in chat_c['participants_id'] and str(target_id) in chat_c['participants_id']) and chat_c[
                'chat_type'] == 'person':
                founded_chat_id = chat_c["chat_id"]
    if founded_chat_id == None:

        random_num = random.randint(2345678909800, 9923456789000)

        new_chat_id = modelInstance_ch.objects.filter(chat_id=random_num)

        while new_chat_id:
            random_num = random.randint(2345678909800, 9923456789000)
            if not modelInstance_ch.objects.filter(chat_id=random_num):
                break

        f.append({
            "chat_id": random_num,
            "participants_id": [res_id, target_id],
            "chat_type": "person"
        })

        tf.append({
            "chat_id": random_num,
            "participants_id": [target_id,res_id],
            "chat_type": "person"
        })

        modelInstance.objects.filter(user_id=res_id).update(user_chats_id=f)
        modelInstance.objects.filter(user_id=target_id).update(user_chats_id=tf)

        chat_info = {
            "chat_id": random_num,
            "chat_type": "person",
            "participants":json.dumps([res_id,target_id]),
            "messages": "[]",
            "group_name":"None",
            "group_description":"None",
            "group_image":"None"
        }

        serializedMessage = chatBoxSerializers(data=chat_info)

        if serializedMessage.is_valid():
            serializedMessage.save()
            return Response(chat_info)
    else:

        return Response({
            "chat_id": founded_chat_id
        })

    return Response({})


def downloadImage(requests):
    BASE_DIR = Path(__file__).resolve().parent.parent

    file_path = "D:\DjangoProjectA\whatsAppBackend\wtsappB\\files\images\890444.png"
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/kl.png")
            response['Content-Disposition'] = 'inline; filename=hj.png'
            return response
    raise Http404

@api_view(["GET"])
def checkUserByPhone(requests,phone_number):
    allDatas = list(userDatasSerializers(modelInstance.objects.all(), many=True).data)
    return Response({"user_exist":isUserExist(allDatas,correctedPhoneNumber(phone_number))})





@api_view(["POST"])
def getUsersByPhoneNumber(requests):
    allDatas = list(userDatasSerializers(modelInstance.objects.all(), many=True).data)
    valid_numebrs = []


    for number in json.loads(requests.data["phone_numbers"]):

        for user in allDatas:
            if number == user["phone_number"]:

                if user not in valid_numebrs:
                    if user["profile_image_id"]!=-1:
                        image_subdirectory=imageBoxSerializers(modelInstance_im.objects.get(image_id=user["profile_image_id"])).data
                        user["profile_image_id"]=image_subdirectory
                        print(user)
                    valid_numebrs.append(user)
                    break

    return Response(valid_numebrs)

@api_view(["GET"])
def ImageUrlByImageId(image_id):
    founded_imageBox = imageBoxSerializers(modelInstance_im.objects.get(image_id=image_id)).data
    return Response({"subDirectory":founded_imageBox})

def isUserExist(users, phone_number):
    for user in users:
        if str(user['phone_number']) == phone_number:
            return True
    return False


@api_view(["POST"])
def login(requests):




    # del requests.data["profile_photo"]


    allDatas = list(userDatasSerializers(modelInstance.objects.all(), many=True).data)

    if isUserExist(allDatas, correctedPhoneNumber(requests.data["phone_number"])):
        user_id = userDatasSerializers(modelInstance.objects.get(phone_number= correctedPhoneNumber(requests.data["phone_number"]))).data[
            "user_id"]

        return Response(
            {
                "user_exist": True,
                "user_id": user_id
            }
        )

    else:

        new_user_id = generate_user_id()
        new_chat_id=generate_group_image_id()
        data = requests.data.dict()

        data["user_id"] = str(new_user_id)
        data ["phone_number"]=correctedPhoneNumber(data["phone_number"])

        if "profile_image" in data:
            data["profile_image_id"] = str(new_chat_id)

        serializedMessage = userDatasSerializers(data=data)

        if serializedMessage.is_valid():
            if "profile_image_id" in data:
                image_name = datetime.datetime.now().microsecond
                image_to_save = ContentFile(base64.b64decode(requests.data.get("profile_image")), name=str(image_name)+".png")
                image = modelInstance_im(upload=image_to_save, image_id=new_chat_id)
                image.save()
            serializedMessage.save()



        return Response(serializedMessage.data)



@api_view(["POST"])
def exitGroup(requests):
    user_id_exit=requests.data.dict()["user_id"]
    chat_id=requests.data.dict()["chat_id"]

    dt = userDatasSerializers(modelInstance.objects.get(user_id=user_id_exit)).data

    user_chats_id=json.loads(dt["user_chats_id"].replace("\'", "\""))
    updated_user_chats_id=[chid for chid in user_chats_id if chid["chat_id"]!=int(chat_id)]

    modelInstance.objects.filter(user_id=user_id_exit).update(user_chats_id=updated_user_chats_id)

    chat_box = chatBoxSerializers(modelInstance_ch.objects.get(chat_id=chat_id)).data
    participants=json.loads(chat_box["participants"].replace("\'","\""))
    updated_participants=[member for member in participants if member["user_id"]!=user_id_exit]
    modelInstance_ch.objects.filter(chat_id=chat_id).update(participants=updated_participants)
    addMessage(chat_id,dt["username"]+" Left","",user_id_exit,"exit_group")




    return Response({})


@api_view(["GET"])
def pvOtherSide(requests,user_id,chat_id):
    sides=getChatParticipants(chat_id)

    otherSide=list(filter(lambda x:x!=user_id,sides))[0]
    print(otherSide)
    return Response({
        "other_side":otherSide
    })


@api_view(["POST"])
def createGroup(requests):




    chat_id = generate_group_chat_id()
    participants = requests.data["participants"]
    group_name = requests.data["group_name"]
    group_description = requests.data["group_description"]
    group_image = requests.data["group_image"]

    if "group_image" in requests.data.dict():
        group_image_id=generate_group_image_id()


    group_temp = {
        "participants": participants,
        "group_name": group_name,
        "group_description": group_description,
        "group_image_id": group_image_id,
        "chat_type": "group",
        "messages": json.dumps([{'sent_message': 'group created', 'time_created': str(datetime.datetime.now()),'message_type':'init_group'}]),
        "chat_id": chat_id
    }

    for user in json.loads(participants.replace("\'","\"")):


        dt = userDatasSerializers(modelInstance.objects.get(user_id=user["user_id"])).data

        user_chats_id = json.loads(dt["user_chats_id"].replace("\'", "\""))
        print(user_chats_id)
        iTemp={'chat_id': chat_id, 'chat_type': 'group'}
        user_chats_id.append(iTemp)
        modelInstance.objects.filter(user_id=user["user_id"]).update(user_chats_id=user_chats_id)

    serializedGroupSettings = chatBoxSerializers(data=group_temp)

    if serializedGroupSettings.is_valid():
        if "group_image" in requests.data.dict():
            image_name = datetime.datetime.now().microsecond
            image_to_save = ContentFile(base64.b64decode(requests.data.get("group_image")), name=str(image_name) + ".png")
            image = modelInstance_im(upload=image_to_save, image_id=group_image_id)
            image.save()
        serializedGroupSettings.save()

    return Response(serializedGroupSettings.data)
