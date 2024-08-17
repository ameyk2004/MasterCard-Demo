from .models import Volunteer, Task, Project
from rest_framework import serializers

class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TaskGetSerializer(serializers.ModelSerializer):
    volunteers = VolunteerSerializer(many=True, read_only = True)
    project  = ProjectSerializer(read_only = True)
    class Meta:
        model = Task
        fields = '__all__'

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


