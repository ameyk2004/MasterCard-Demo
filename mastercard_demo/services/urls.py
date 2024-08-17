from django.urls import path, include
from . import views

urlpatterns = [
    path('tasks/', views.TaskGet.as_view(), name="task-create"),
    path('tasks/<int:pk>/', views.TaskDetail.as_view(), name="task-retrieve"),
    path('tasks/<int:pk>/update', views.TaskUpdate.as_view(), name="task-update"),
    path('volunteers/', views.TaskCreate.as_view(), name="volunteer-create"),
]
