
from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Create your models here.
class Task(models.Model):
    title = models.CharField(blank=True,max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)  

    def __str__(self):
        return self.title