from rest_framework.serializers import Serializer, ModelSerializer 
from rest_framework import serializers
from .models import Task
from django.utils import timezone
from zoneinfo import ZoneInfo
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class UserSerializer(serializers.Serializer):

    id = serializers.UUIDField(read_only = True)
    phone_number = serializers.CharField(required = True)
    # username = serializers.CharField(required = True)
    bio = serializers.CharField(read_only = True)
    created_at = serializers.DateTimeField(read_only = True)
    password = serializers.CharField(required = True, write_only = True)
    created_at = serializers.DateTimeField(read_only = True)

    def create(self, validated_data):
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