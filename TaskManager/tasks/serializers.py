from rest_framework.serializers import Serializer, ModelSerializer 
from rest_framework import serializers
from .models import Task, Users
from django.utils import timezone
from zoneinfo import ZoneInfo


# we have to write the field types and the create, update logic
class TaskSerializer(Serializer):
    
    # read_only only makes us read the data from the model not the opposite
    id = serializers.UUIDField(read_only = True)
    name = serializers.CharField(required = True)
    description = serializers.CharField(required = False)
    completed = serializers.BooleanField(required = False)
    completed_at = serializers.DateTimeField(required = False)
    deadline = serializers.DateTimeField(required = False)
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
        fields = "__all__"
    # field validation
    # object validation can be added to the data

    def create(self, validated_data):
        # perform manipulation on the validated_data before the create
        return super().create(validated_data)
    
    # instance is the real object and validated_data is the to be changed to reocrd
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)