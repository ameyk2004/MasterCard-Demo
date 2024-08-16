from django.db import models

# Create your models here.
# 1. Volunteers who register to help with various projects.
# 2. Projects that the NGO is working on.
# 3. Tasks under each project that volunteers can sign up for.
# 4. Volunteer-Task Assignments where multiple volunteers can sign up for the same task, and each task can have multiple volunteers.


# Volunteer 1 - > 1, 2 , 4
# Volunteer 1 - > 1, 3 , 4
# Task 1, 2 - > proj 1
# task 3, 4 -> proj 2

class Volunteer(models.Model):
    id = models.IntegerField(primary_key=True) 
    name = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name}"


class Project(models.Model):
    proj_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.name}"


class Task(models.Model):
    task_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    volunteers = models.ManyToManyField(Volunteer)

    def __str__(self) -> str:
        return f"{self.name}"