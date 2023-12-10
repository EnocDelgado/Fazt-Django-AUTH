from django.db import models
from django.contrib.auth.models import User

# Define a Task model that inherits from Django's Model class
class Task(models.Model):
    
    # Define fields for the Task model
    
    # Title of the task
    title = models.CharField(max_length=100)                
    # Description of the task (optional)
    description = models.TextField(blank=True)              
    # Date and time when the task is created
    created = models.DateTimeField(auto_now_add=True)       
    # Date and time when the task is completed (nullable)
    datecompleted = models.DateTimeField(null=True)         
    # Indicates whether the task is marked as important
    important = models.BooleanField(default=False)         
    # Foreign key relationship with the User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)  

    # Define a string representation for the Task model
    def __str__(self):
        return self.title + " - by " + self.user.username