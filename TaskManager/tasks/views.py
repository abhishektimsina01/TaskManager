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

@api_view(['POST'])
def postTask(request):
    # we need to send the request.data to the serializer for validation and save it
    pass