from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import getAllTodos, postTask, getTask, deleteTask, editTask

router = DefaultRouter()


urlpatterns = [
     path('getAll/', getAllTodos),
     path("getOne/<int:id>/", getTask),
     path("postTask/", postTask),
     path("editTsak/<int:id>/", editTask),
     path("deleteTask/<int:id>/", deleteTask)
]
