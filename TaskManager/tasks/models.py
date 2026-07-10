from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime, time
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
import uuid

# Create your models here.

# creating my own User model so that i can add extra fields in the User model except the one that is provided
class CustomUser(AbstractUser):
    # we have already got many properties and methods that allows us create and 
    # perform different operations like set_password etc
    # AbstractBaseUser --> AbstractUser <-- PermissionMixins
    username = None
    phone_number = models.CharField(max_length=10, unique=True)
    bio = models.CharField(max_length=50, null= True)
    
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []


# user model
class Users(models.Model):
    # enum
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("user", "User")
    ]
    id = models.UUIDField(primary_key= True, default= uuid.uuid4)
    username = models.CharField(max_length=20, db_index= True, unique=True)
    password = models.CharField(max_length=20)
    role = models.CharField(choices= ROLE_CHOICES, default="user")
    created_at = models.DateTimeField(auto_now=True)
    
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
    user_id = models.ForeignKey(Users, on_delete= models.CASCADE)