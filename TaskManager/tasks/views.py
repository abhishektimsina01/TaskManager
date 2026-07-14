from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskModelSerializer, TaskSerializer, UserSerializer, MyTokenObtainSerializer, MyTokenRefreshSerializer, MyTokenBlackListSerializer
from datetime import timedelta, datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from zoneinfo import ZoneInfo
from django.contrib.auth import get_user_model
UsersModel = get_user_model()

# Create your views here:-  

# **********************************************************************************************************************
# Function based view(FBV):
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllTodos(request):
    print('User information')
    print(request.user.password)
    # request object contains all the information baout the http request done by the user
    print(request.GET)
    # all() means get all the objects/records from the table
    tasks = Task.objects.all()
    # task is a complicated datatype so we need to serialize it
    serialized = TaskSerializer(tasks, many = True)
    print(serialized.data)
    return Response(data = serialized.data, status = status.HTTP_202_ACCEPTED)


# get the specific task of id = id
@api_view(['GET'])
def getTask(request, id):
    try:
        print(timezone.now())
        print(request.GET)
        task = Task.objects.get(id = id)
    except Task.DoesNotExist:
        return Response({'error' : 'does not exist'}, status= status.HTTP_404_NOT_FOUND)
    serialized = TaskSerializer(task)
    if not serialized.data.get("completed"):
        # for GMT +5:45 offset for current time
        ktm = ZoneInfo("Asia/Kathmandu")
        deadline = serialized.data.get("deadline")
        # parse_datetime is used to parse the string date to timezone
        deadline = parse_datetime(deadline).astimezone(ktm).replace(tzinfo=None)
        # convert the timezone from 00:00 to 05:45 for match logically
        current_time = timezone.now().astimezone(ktm).replace(tzinfo=None)
        # instead of using the current_time, we can use the datetime.now() as we dont have to replace the 
        print(current_time, datetime.now())
        print(deadline,"\n",current_time)
        if deadline > current_time:
            difference = deadline - current_time
            print(deadline - current_time)
            return Response({'data' : serialized.data, "status" : "the task is not completed yet. there is still time left", "deadline" : str(deadline), "current time" : str(current_time), "time left": f"{difference}"})
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
    allSerialized = TaskModelSerializer(allTasks, many = True)
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
    
    # original instance
    before_change = TaskSerializer(task)
    print("Original Data")
    print(before_change.data)
    serialized = TaskSerializer(instance = task, data = request.data, partial = True)
    if not serialized.is_valid():
        return Response(serialized.errors)
    serialized.save()
    return Response(serialized.data)


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


# class based view
class Users(APIView):

    # in APIView, we can only use all the htpp methods ones and not more than one
    def get(self, request):
        print("get request")
        print(request.GET)
        users = UsersModel.objects.all()
        print(users)
        serialized = UserSerializer(users, many = True)
        print(serialized.data)
        return Response(serialized.data)

    def post(self, request):
        print("*"*10, "creating user", "*"*10)
        print(request.data)
        # return Response(request.data)
        serialized = UserSerializer(data = request.data)
        print(serialized.is_valid())
        if serialized.is_valid():
            a = serialized.save()
            print(type(a))
            print(a.id)
            print(a.username)
            token = RefreshToken.for_user(a)
            print(token.access_token)
            response = Response({"data" : serialized.data,
                                  "access_token" : str(token.access_token), 
                                  'refresh_token' : str(token)
                                })
            response.set_cookie(
                key = "access_token",
                value = str(token.access_token),
                httponly = True,
                secure = False,
                max_age = 60*10
            )
            response.set_cookie(
                key = "refresh_token",
                value = str(token),
                httponly=True,
                secure=True,
                max_age=60*60*24
            )
            return response
        else:
            return Response(serialized.errors)

    def patch(self, request, id):
        print(request.data)
        try:
            user = UsersModel.objects.get(id = id)
        except UsersModel.DoesNotExist:
            return Response({'error': 'user doesnot exist'})
        user_org = UserSerializer(user)
        print(user_org.data)
        serialized = UserSerializer(instance = user, data = request.data, partial = True)
        if not serialized.is_valid():
            return Response({serialized.errors})
        print(serialized.is_valid())
        serialized.save()
        return Response(serialized.data)
    
    def delete(self, request):
        users = UsersModel.objects.all()
        serialized = UserSerializer(users, many = True)
        users.delete()
        return Response({'users' : serialized.data, 'message' : 'deleted all users'})

@api_view(['GET'])
def getUserTask(request, id):
    try:
        user = UsersModel.objects.get(id = id)
    except UsersModel.DoesNotExist:
        return Response({'error': "No user with that id"})
    user_serialized = UserSerializer(user)
    print(user_serialized.data)

    # filter all the task that is made by the user
    tasks = Task.objects.filter(user_id = id)
    tasks_serialized = TaskSerializer(tasks, many = True)
    for task in tasks_serialized.data:
        task.pop("user")
    return Response({ "user" : user_serialized.data, 'task' : tasks_serialized.data})



# the goal is to provide the user cookie when the user logs in rather than the JSON data:
class LogIn(TokenObtainPairView):
    # for my own login endpoint view i need my own serializer class
    serializer_class = MyTokenObtainSerializer
    # we need to apply the cookie to send the token not the JSON so we overide the POST method
    def post(self, request, *args, **kwargs):
        print(request.data)
        response = super().post(request, *args, **kwargs)
        print(7)
        print(response)
        access = response.data.get("access")
        refresh = response.data.get("refresh")
        response.set_cookie(
                key = "access_token",
                value = access,
                httponly = True,
                secure = False,
                max_age = 60*10
                )
        response.set_cookie(
            key = "refresh_token",
            value = refresh,
            httponly=True,
            secure=True,
            max_age=60*60*24
            )
        response.data.pop("access", None)
        response.data.pop("refresh", None)
        return response


# validates the refresh_token and send the access_token in the form of the cookie
class Refresh(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        # before sending the token, i need to take the cookie from the cookie and set it in request.data
        
        reponse = super().post(request, *args, **kwargs)


# takes the refresh-token in the form of cookie, 
# valiates the refrresh_token, 
# blacklist the token and remove the cookies
class LogOut(TokenBlacklistView):
    serializer_class = MyTokenBlackListSerializer

    def post(self, request, *args, **kwargs):
        # before sending the 
        return super().post(request, *args, **kwargs)