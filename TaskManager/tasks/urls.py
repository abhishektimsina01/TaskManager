from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import getAllTodos, postTask, getTask, deleteTask, editTask, deleteAll, completedTask, getUserTask, logoutUser
from .views import Users, LogIn
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

router = DefaultRouter()


urlpatterns = [
     path('getAll/', getAllTodos),
     path("getOne/<uuid:id>/", getTask),
     path("completedTask/", completedTask),
     path("postTask/", postTask),
     path("editTask/<uuid:id>", editTask),
     path("deleteTask/<uuid:id>/", deleteTask),
     path("deleteAll/", deleteAll),

     path("getUsers/", Users.as_view()),
     path("addUser/", Users.as_view()),
     path("editUser/<uuid:id>", Users.as_view()),
     path("deleteUsers/", Users.as_view()),

     path("getUserTasks/<uuid:id>/", getUserTask),

     path("logoutUser/", logoutUser),
     
     # for authentication
     path("login/", LogIn.as_view()),
     path("logout/", logoutUser),
     # path("login/", TokenObtainPairView.as_view()),
     path("refresh/", TokenRefreshView.as_view()),
]