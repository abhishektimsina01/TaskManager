from rest_framework.serializers import Serializer, ModelSerializer 
from rest_framework import serializers
from .models import Task, Users

class TaskSerializer(Serializer):

    id = serializers.UUIDField(required = True)
    name = serializers.CharField(required = True)
    description = serializers.CharField()
    completed = serializers.BooleanField()
    deadline = serializers.DateTimeField()

    # is called when the .save() is called after proper validation 
    def create(self, validated_data):
        return Task.objects.create(**validated_data)
    
    # similarly but should be passed the instance and the partial = True
    def update(self, instance, validated_data):
        # it works both for the partial as well as the full update as it uses the 
        instance['name'] = validated_data.get('name', instance['name'])
        instance['description'] = validated_data.get('description', instance['description'])
        instance['completed'] = validated_data.get('completed', instance['completed'])
        instance['deadline'] = validated_data.get("deadline", instance['deadline'])
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