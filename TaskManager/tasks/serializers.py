from rest_framework.serializers import Serializer, ModelSerializer 
from rest_framework import serializers
from .models import Task
from django.utils import timezone
from zoneinfo import ZoneInfo
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

CustomUser = get_user_model()   


class UserSerializer(serializers.Serializer):

    id = serializers.UUIDField(read_only = True)
    username = serializers.CharField(required = True)
    phone_number = serializers.CharField(required = False)
    bio = serializers.CharField(required = True)
    created_at = serializers.DateTimeField(read_only = True)
    password = serializers.CharField(required = True, write_only = True)
    created_at = serializers.DateTimeField(read_only = True)

    def create(self, validated_data):
        # creating the user
        return CustomUser.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        # instance is the real data and validated_data is the data sent by the user
        instance.username = validated_data.get("username", instance.username)
        instance.set_password(validated_data.get("password", instance.password))
        instance.role = validated_data.get("role", instance.role)
        instance.save()
        return instance


# we have to write the field types and the create, update logic
class TaskSerializer(Serializer):
    
    # read_only only makes us read the data from the model not the opposite
    # required = True/False
    # read_only = True/False
    # write_only = True/False
    id = serializers.UUIDField(read_only = True)
    name = serializers.CharField(required = True)
    description = serializers.CharField(required = False)
    completed = serializers.BooleanField(required = False)
    completed_at = serializers.DateTimeField(required = False)
    deadline = serializers.DateTimeField(required = False)
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only = True)
    user = UserSerializer(source = "user_id", read_only = True)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    # is called when the .save() is called after proper validation 
    def create(self, validated_data):
        return Task.objects.create(**validated_data)
    
    # similarly but should be passed the instance and the partial = True
    def update(self, instance, validated_data):
        ktm = ZoneInfo("Asia/Kathmandu")
        print(instance)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        if not validated_data.get("completed", False):
            # if not given
            instance.completed = False
            instance.completed_at = None
        else:
            # if given
            instance.completed = True
            instance.completed_at = timezone.now()

            print("completed time", instance.completed_at)
        instance.deadline = validated_data.get("deadline", instance.deadline)
        instance.save()
        return instance


# create and update is already built-in, we only have build it if we want to customize
class TaskModelSerializer(ModelSerializer):
    class Meta:
        model = Task
        # field is all the fields to include
        fields = "__all__"
        # we dont have to send
        read_only_fields = ["id", "created_at", "updated_at"]
    
    # we can perform the overwrtie of the data if we want to by using the create and updateand then again pass it to the super().create() and super().update()
    def create(self, validated_data):
        # perform manipulation on the validated_data before the create
        return super().create(validated_data)
    
    # instance is the real object and validated_data is the to be changed to reocrd
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

class TokenObtainSerializer(TokenObtainPairSerializer):
    # the TokenObtainPairSerializer allows us the validate method, which takes the username + password
    # it authneticates it, gets the user, generates the tokens(access and refesh)
    # provide us the tokens
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)
        # now we can add all the required fields in the token which can be used by the frontend
        # token['phone_number'] = user.phone_number
        # token["bio"] = user.bio
        return token
    
    # attrs is the dictionary that contains the attribute of the data that we need to validate/authenticate
    def validate(self, attrs):
        data = super().validate(attrs)
        # data contains the access and refresh token, we can send additional data to it
        # we get the information of the user from the self.user after the authenticte() method executes
        # we can add the user informaton to it, which can be used by the views
        # which can be sent as the response after the access and the refresh token is removed
        data["user"] = {
            "id" : self.user.id,
            "username" : self.user.username
        }
        # now data contains the information + tokens (access and refresh)
        return data