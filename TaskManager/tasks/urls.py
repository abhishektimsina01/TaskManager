from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import getAllTodos, postTask, getTask, deleteTask, editTask, deleteAll, completedTask

router = DefaultRouter()


urlpatterns = [
     path('getAll/', getAllTodos),
     path("getOne/<uuid:id>/", getTask),
     path("completedTask/", completedTask),
     path("postTask/", postTask),
     path("editTask/<uuid:id>", editTask),
     path("deleteTask/<uuid:id>/", deleteTask),
     path("deleteAll/", deleteAll)
]