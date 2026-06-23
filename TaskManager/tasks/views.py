from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from .models import Task, Users
from .serializers import TaskModelSerializer, TaskSerializer
from datetime import timedelta, datetime

# Create your views here:- 

# **********************************************************************************************************************
# Function based view(FBV):
@api_view(['GET'])
def getAllTodos(request):
    # request object contains all the information baout the http request done by the user
    print(request.GET)
    # all() means get all the objects/records from the table
    tasks = Task.objects.all()
    # task is a complicated datatype so we need to serialize it
    serialized = TaskModelSerializer(tasks, many = True)
    print(serialized.data)
    return Response(data = serialized.data, status = status.HTTP_202_ACCEPTED)


# get the specific task of id = id
@api_view(['GET'])
def getTask(request, id):
    try:
        print(request.GET)
        task = Task.objects.get(id = id)
    except Task.DoesNotExist:
        return Response({'error' : 'does not exist'}, status= status.HTTP_404_NOT_FOUND)
    serialized = TaskSerializer(task)
    if not serialized.data.get("completed"):
        # calculate the time left
        deadline = serialized.data.get("deadline")
        current_time = datetime.now()
        print({"current time" : datetime.now(), "deadline" : deadline})
        return Response({'data' : serialized.data, "status" : "the task is not completed yet", "time left" : f""})
    # print(serialized.data)
    return Response({'data' : serialized.data, "status" : f"the task is completed."}, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def postTask(request):
    print(datetime.now())
    print(request.POST)
    print(request.data)
    serialized = TaskSerializer(data = request.data)
    # serialized.is_valid() checks for all the validation (model based validation, custom field validation, object validation)
    if not serialized.is_valid():
        return Response(serialized.errors)
    else:
        # if everything is valid then we save it to create()
        serialized.save()
        return Response(serialized.data)


@api_view(['PUT'])
def editTask(request, id):
    try:
        task = Task.objects.get(id = id)
    except Task.DoesNotExist:
        return Response({'error' : 'does not exist'})
    serialized = TaskSerializer(task, data = request.data, partial = True)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data)
    return Response(serialized.errors)


@api_view(['DELETE'])
def deleteTask(request, id):
    try:
        print(request.DELETE)
        task = Task.objects.get(id = id)
    except Task.DoesNotExist:
        return Response({'error' : 'was not found or multiple found'})
    serialized = TaskSerializer(task)
    # the task exist so we delete the record
    task.delete()
    return Response({"data " : serialized.data, "message" : "Task deleted"})

@api_view(['DELETE'])
def deleteAll(request):
    all_tasks = Task.objects.all()
    serialized = TaskModelSerializer(all_tasks, many = True)
    print(serialized.data)
    Task.objects.all().delete()
    return Response({'data': serialized.data, 'message' : "deleted all"})   