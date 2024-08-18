from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . views import RegisterView, TaskDetail, TaskListCreateView, ProjectListCreateView


urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('tasks/', TaskListCreateView.as_view(), name='task-listcreate'),
    path('tasks/<int:pk>', TaskDetail.as_view(), name='task-detail'),
    path('projects/', ProjectListCreateView.as_view(), name='project-listcreate'),
]
