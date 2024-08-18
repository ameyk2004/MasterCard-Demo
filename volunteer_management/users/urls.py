from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . views import RegisterView, TaskDetail, TaskListCreateView, ProjectListCreateView, register_for_task


urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('tasks/', TaskListCreateView.as_view(), name='task-listcreate'),
    path('tasks/<int:pk>', TaskDetail.as_view(), name='task-detail'),
    path('tasks/<int:pk>/register/', register_for_task, name='task-register'),
    path('projects/', ProjectListCreateView.as_view(), name='project-listcreate'),
]
