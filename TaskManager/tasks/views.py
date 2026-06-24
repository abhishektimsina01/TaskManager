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
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from zoneinfo import ZoneInfo

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
        for i in request.query_params:
            print(i, request.query_params.get(i))
        task = Task.objects.get(id = id)
    except Task.DoesNotExist:
        return Response({'error' : 'does not exist'}, status= status.HTTP_404_NOT_FOUND)
    serialized = TaskSerializer(task)
    if not serialized.data.get("completed"):
        # for GMT +5:45 offset for current time
        ktm = ZoneInfo("Asia/Kathmandu")
        deadline = serialized.data.get("deadline")
        # parse_datetime is used to parse the string date to timezone
        deadline = parse_datetime(deadline).replace(tzinfo=None)
        # convert the timezone from 00:00 to 05:45 for match logically
        current_time = timezone.now().astimezone(ktm).replace(tzinfo=None)
        # instead of using the current_time, we can use the datetime.now() as we dont have to replace the 
        print(current_time, datetime.now())
        print(deadline,"\n",current_time)
        if deadline > current_time:
            difference = deadline - current_time
            print(deadline - current_time)
            return Response({'data' : serialized.data, "status" : "the task is not completed yet. there is still time left", "time left": f"{difference}"})
        return Response({'data' : serialized.data, "status" : "the task is not completed yet. deadline expired", "time left" : f"0"})
    
    completed_time = serialized.data.get("completed_at")
    return Response({'data' : serialized.data, "status" : f"the task is completed.", "time left" : f"{completed_time}"}, status=status.HTTP_202_ACCEPTED)


# completed and not_completed task
@api_view(['GET'])
def completedTask(request):
    print(request.GET)
    tasks = Task.objects.filter(completed = True)
    allTasks = Task.objects.all()
    completedSerialized = TaskSerializer(tasks, many = True)
    print(completedSerialized.data)
    allSerialized = TaskSerializer(allTasks, many = True)
    print(allSerialized.data)
    print("="*100)
    completedTask = []
    notCompletedTask = []
    for task in allSerialized.data:
        if task.get("completed"):
            completedTask.append(task)
        else:
            notCompletedTask.append(task)
    print("="*100)
    return Response({'not completed' : notCompletedTask, "completed" : completedTask})


# post the data
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
        print(serialized.data.get('id'))
        return Response(serialized.data)


@api_view(['PUT'])
def updateTask(request, id):
    try:
        task = Task.objects.get(id = id)
    except Task.DoesNotExist:
        return Response({'error' : 'does not exist'})
    serialized = TaskSerializer(task, data = request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data)
    return Response(serialized.errors)

# partial update
@api_view(['PATCH'])
def editTask(request, id):
    try:
        task = Task.objects.get(id = id)
    except Task.DoesNotExist:
        return Response({'error' : "no record with the id found"})
    print("given partial data", request.data)
    return Response(request.data)


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