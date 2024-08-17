# NGO - Volunteer management system

```
An NGO is looking to manage its volunteer activities. They want a system where they can track the following:

1. Volunteers who register to help with various projects.
2. Projects that the NGO is working on.
3. Tasks under each project that volunteers can sign up for.
4. Volunteer-Task Assignments where multiple volunteers can sign up for the same task, and each task can have multiple volunteers.
```

## Step 1 - Designing ER Model

1. Understaing Etities and Relations

### Entities in Project

1. Volunteer (id, name, age, email, password)
2. Projects (proj_id, description, start_date, end_end_date)
3. Tasks (task_id, proj_id, name, description)


<img src = "notes_assets/Screenshot 2024-08-16 at 8.57.39 AM.png">

## Step 2 - Implimenting Models in Django


```python
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
```







