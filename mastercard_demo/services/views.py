from django.shortcuts import render
from .serializers import TaskCreateSerializer, TaskGetSerializer
from .models import Volunteer, Task, Project

from rest_framework import generics


class TaskGet(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskGetSerializer

class TaskCreate(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

class TaskDetail(generics.RetrieveDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskGetSerializer

class TaskUpdate(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer


