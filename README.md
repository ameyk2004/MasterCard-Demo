# NGO - Volunteer management system

```
An NGO is looking to manage its volunteer activities. They want a system where they can track the following:

1. Volunteers who register to help with various projects.
2. Projects that the NGO is working on.
3. Tasks under each project that volunteers can sign up for.
4. Volunteer-Task Assignments where multiple volunteers can sign up for the same task, and each task can have multiple volunteers.
```

## Step 1 : Initiating the Project

a. Create and activate a virtual environment:
```bash
# Navigate to your desired directory
cd ~/projects

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```


b. Install Django and necessary packages:

```bash
# Install Django and Django REST Framework
pip install django djangorestframework

# Install Simple JWT for JWT token authentication
pip install djangorestframework-simplejwt

```

c. Create a new Django project:

```bash
# Create the Django project
django-admin startproject VolunteerManagement

# Navigate into the project directory
cd VolunteerManagement
```

## Step 2 : Add the apps and REST framework to INSTALLED_APPS in settings.py:

- Open VolunteerManagement/settings.py and add the following:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'users',
]
```

3. Install and Configure Simple JWT
In settings.py, configure JWT authentication:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Simple JWT Settings (Optional: You can customize these)
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

4. Create a Custom User Model
In the users app, create a models.py file with the custom user model.

a. Define the CustomUser model:

```python
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('coordinator', 'Coordinator'),
        ('volunteer', 'Volunteer'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='volunteer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return self.email
```

b. Update the settings.py to use the custom user model:

```python
AUTH_USER_MODEL = 'users.CustomUser'
```

## Step 2: Implement User Registration and Authentication APIs

In this step, you'll create the necessary API endpoints for user registration and authentication (login) using Django REST Framework and Simple JWT.

### 1. Create Serializers for User Registration and Authentication
In the users app, create a file named serializers.py and define the following serializers:

a. User Registration Serializer:

```python
from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'role', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user
```

b. User Detail Serializer:
This serializer will be used to return user details after successful registration or login.

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'role']
```

2. Create Views for Registration and Authentication
In the users app, create a file named views.py and define the views for registration and authentication:

**a. User Registration View:**

```python
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_201_CREATED)

```

- The create() method in the RegisterView class is an override of the create() method provided by Django REST Framework's CreateAPIView. While it's not strictly necessary to override this method, doing so allows you to customize the behavior of the view when a new user is being registered.

- Why the create() Method is Overridden:
Customizing the Response:

- By default, CreateAPIView would create the object and return a response with the serialized data. However, you might want to modify the response data or status code, or include additional logic before returning the response.
In your custom create() method, after saving the user, you serialize the user data again using UserSerializer and return that data in the response. This can be useful if you want to control exactly what data is sent back to the client after registration.

**b. JWT Authentication View:**
You can use the built-in views provided by rest_framework_simplejwt. Add these imports in views.py:

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
```

3. Create URLs for User Registration and Authentication
In the users app, create a file named urls.py and define the following routes:

```python
from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

4. Include User URLs in the Main Project URLs
Open VolunteerManagement/urls.py and include the users app URLs:

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
]
```

5. Test the APIs
Now, run the Django development server:

```bash
python manage.py runserver
```

You can use tools like Postman or curl to test the registration and login APIs:

a. Register a New User:
Endpoint: POST http://127.0.0.1:8000/api/users/register/

Payload:

```json
{
    "email": "johndoe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "volunteer",
    "password": "strongpassword"
}
```


Expected Response:

```json
{
    "id": 1,
    "email": "johndoe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "volunteer"
}
```

b. Obtain JWT Tokens (Login):
Endpoint: POST http://127.0.0.1:8000/api/users/login/

Payload:

```json
{
    "email": "johndoe@example.com",
    "password": "strongpassword"
}
```

Expected Response:

```json
{
    "refresh": "your-refresh-token",
    "access": "your-access-token"
}
```

## Step 3: Implement Task Management with Relational Models

Now that user registration and authentication are set up, let's implement the core feature of the application: Task Management. We'll create models for tasks and establish relationships between tasks, users (volunteers, coordinators), and projects.

**1. Define the Models**
In the users app, create models for Project and Task. These models will establish the relationships between tasks and users.

a. Update models.py in the users app:

```python
from django.db import models
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

```

**2. Make and Apply Migrations**
After defining the models, create and apply the migrations:
```bash
# Create migrations for the new models
python manage.py makemigrations users

# Apply the migrations to the database
python manage.py migrate
```

**3. Create Serializers for Task and Project**
Create serializers for the Task and Project models in serializers.py to handle data input and output.

a. Add the following in serializers.py:

```python
from .models import Project, Task

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date']

class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'project', 'assigned_to', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        task = Task.objects.create(created_by=request.user, **validated_data)
        return task

```

**4. Create Views for Task and Project Management**

In views.py, create views to handle CRUD operations for tasks and projects.

a. Define the views in views.py:

```python
from rest_framework import generics, permissions
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'volunteer':
            return self.queryset.filter(assigned_to=user)
        elif user.role == 'coordinator' or user.role == 'admin':
            return self.queryset.all()

```

**5. Create URLs for Task and Project Management**

Add the URLs for the task and project management views in users/urls.py:

```python
from django.urls import path
from .views import ProjectListCreateView, TaskListCreateView, TaskDetailView

urlpatterns += [
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
```


**6. Test the Task and Project APIs**

Run the Django development server and test the new APIs.

a. Create a New Project:
Endpoint: POST http://127.0.0.1:8000/api/users/projects/

Payload:

```json
{
    "name": "Community Outreach",
    "description": "Outreach program to connect with local communities.",
    "start_date": "2024-09-01",
    "end_date": "2024-12-01"
}
```


