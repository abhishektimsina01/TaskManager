from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import getAllTodos

router = DefaultRouter()


urlpatterns = [
     path('/tasks', getAllTodos)
]
