from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import getAllTodos, postTask, getTask, deleteTask, editTask, deleteAll, completedTask, getUserTask
from .views import Users
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

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

     # for authentication
     path("login/", TokenObtainPairView.as_view()),
     path("refresh/", TokenRefreshView.as_view()),
     path("verify/", TokenVerifyView.as_view())
]