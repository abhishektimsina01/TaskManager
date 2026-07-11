from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime, time
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
import uuid
from .manager import CustomUserManager
from django.conf import settings



# creating my own User model so that i can add extra fields in the User model except the one that is provided
class CustomUser(AbstractUser):
    # we have already got many properties and methods that allows us create and 
    # perform different operations like set_password etc
    # AbstractBaseUser --> AbstractUser <-- PermissionMixins
    id = models.UUIDField(primary_key= True, default = uuid.uuid4)
    username = None
    phone_number = models.CharField(max_length=10, unique=True)
    bio = models.CharField(max_length=50, null= True)
    created_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()



# for the time to complete the task, we can use function to use the timezone and timedelta
def default_deadline():
    return timezone.now() + timedelta(hours= 24)    


# task model
class Task(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4)
    name = models.CharField(max_length=50)
    description = models.TextField(default = "")
    completed = models.BooleanField(default= True)

    # target time to complete
    deadline = models.DateTimeField(default = default_deadline)

    # completed at
    # set to the time when the task is completed, completed is set to True
    completed_at = models.DateTimeField(null= True)

    # auto_now_add = True means when it is created then the time at that moment
    created_at = models.DateTimeField(auto_now_add= True)

    # auto_now = True means when it is updated then the time as that moment
    updated_at = models.DateTimeField(auto_now= True)

    # if the corresponding is user is deleted then the task is also delted from the database
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
