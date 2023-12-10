from django.forms import ModelForm
from .models import Task

# Define a form class TaskForm that inherits from Django's ModelForm
class TaskForm(ModelForm):
    
    # Meta class to specify the associated model and the fields to include in the form
    class Meta:
        # Set the model for the form to be the Task model
        model = Task                   
        # Specify the fields to be included in the form
        fields = ['title', 'description', 'important']  
