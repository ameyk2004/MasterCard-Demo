from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from . models import *
from .serializers import RegisterSerializer, UserSerializer, TaskSerializer, ProjectSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = UserSerializer(user).data

        return Response(user_data, status=status.HTTP_201_CREATED)
    

class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes= [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(reated_by=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes= [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'volunteer':
            return self.queryset.filter(assigned_to=user)
        else:
            return self.queryset.all()




