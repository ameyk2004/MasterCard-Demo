from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from . models import *
from .serializers import RegisterSerializer, UserSerializer, TaskSerializer, ProjectSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .permissions import IsAdminOrCoordinator, IsTaskOwnerOrAdminOrCoordinator
from rest_framework.decorators import api_view, permission_classes


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
    permission_classes= [permissions.IsAuthenticatedOrReadOnly, IsAdminOrCoordinator]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes= [permissions.IsAuthenticatedOrReadOnly, IsTaskOwnerOrAdminOrCoordinator]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'volunteer':
            return self.queryset.filter(assigned_to=user)
        else:
            return self.queryset.all()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_for_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        if task.assigned_to:
            return Response({'detail': 'Task is already assigned.'}, status=status.HTTP_400_BAD_REQUEST)
        task.assigned_to = request.user
        task.save()
        return Response({'detail': 'You have successfully registered for the task.'}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({'detail': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)



