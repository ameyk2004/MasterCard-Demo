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





