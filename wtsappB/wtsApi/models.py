from django.db import models

# Create your models here.



class usersData(models.Model):
    username = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=250)
    user_id = models.IntegerField(default=-1)
    bio = models.TextField(default="Hey there! I am using WhatsApp")
    profile_image_id = models.IntegerField(default=-1)
    user_chats_id = models.TextField()



class messages(models.Model):
    chat_id=models.IntegerField()
    message_id=models.IntegerField()
    sender_id=models.IntegerField()
    time_created=models.TextField(default="2020")
    message=models.TextField()

class chatBox(models.Model):
    CHAT_TYPE=(
        ('group','group'),
        ('person','person')
    )
    chat_id=models.IntegerField(default=-1)
    chat_type = models.TextField(choices=CHAT_TYPE,default='person')
    participants = models.TextField()
    group_name = models.CharField(max_length=30,)
    group_description = models.CharField(max_length=150,)
    group_image_id = models.IntegerField(default=-1)
    messages = models.TextField()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'images/{0}'.format(filename)
class imageBox(models.Model):
    IMAGE_USAGE_CHOSEN=(
        ("post", "post"),
        ("profile","profile"),
        ("group_image","group_photo"),

    )
    image_usage=models.TextField(default="post" ,choices=IMAGE_USAGE_CHOSEN)
    upload = models.ImageField(upload_to=user_directory_path)
    image_id=models.IntegerField(default=-1)



# {
# "username":"armin",
# "phone_number":"09374301779",
# "user_id":12345,
# "image_url":"ssssssssssss",
# "messages":"{}"
# }