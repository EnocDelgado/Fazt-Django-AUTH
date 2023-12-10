from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse  # to create a page and see it on the browser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # Create a Database Model for us
from django.contrib.auth import login, logout, authenticate  # Create Cookie
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

# Home view rendering the home.html template
def home(request):
    return render(request, 'home.html')

# Signup view handling user registration
def signup(request):
    # Validation
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        # Check if passwords match
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Create user based on data provided from the signup form
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])

                # Save in the database
                user.save()
                # Create a cookie
                login(request, user)
                # Redirect to the tasks page
                return redirect('tasks')

            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password does not match'
        })


# Tasks view displaying the tasks for the logged-in user
@login_required
def tasks(request):
    # Get all tasks for the logged-in user where datecompleted is null
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})


# Completed tasks view displaying completed tasks for the logged-in user
@login_required
def tasks_completed(request):
    # Get all tasks for the logged-in user where datecompleted is not null, ordered by datecompleted
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})


# Create task view handling the creation of new tasks
@login_required
def create_task(request):
    # Validation
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            # Get information from the form
            form = TaskForm(request.POST)

            new_task = form.save(commit=False)

            # Save data in the database
            new_task.user = request.user
            new_task.save()

            # Redirect to the tasks page
            return redirect('tasks')

        except ValueError:
            return render(request, 'create_tasks.html', {
                'form': TaskForm,
                'error': 'Please provide valid data'
            })


# Task detail view allowing the user to view and edit a specific task
@login_required
def task_detail(request, task_id):
    # Validation
    if request.method == 'GET':
        # Use get_object_or_404 to avoid a server error if the task doesn't exist
        task = get_object_or_404(Task, pk=task_id, user=request.user)

        # Display the form when the user wants to edit their task
        form = TaskForm(instance=task)

        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            # Use get_object_or_404 to avoid a server error if the task doesn't exist
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            # Invoke TaskForm to receive data from the form
            form = TaskForm(request.POST, instance=task)
            # Save in the database
            form.save()

            return redirect('tasks')

        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': "Error updating task"
            })


# Complete task view marking a specific task as completed
# View for marking a task as completed, restricted to authenticated users
@login_required
def complete_task(request, task_id):
    # Retrieve the task with the specified task_id for the logged-in user
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    # Check if the request method is POST
    if request.method == 'POST':
        # Set the task's datecompleted to the current time
        task.datecompleted = timezone.now()
        # Save the updated task in the database
        task.save()
        # Redirect the user to the 'tasks' page after completing the task
        return redirect('tasks')


# Delete task view allowing the user to delete a specific task
# View for deleting a task, restricted to authenticated users
@login_required
def delete_task(request, task_id):
    # Retrieve the task with the specified task_id for the logged-in user
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    # Check if the request method is POST
    if request.method == 'POST':
        # Delete the task from the database
        task.delete()
        # Redirect the user to the 'tasks' page after deletion
        return redirect('tasks')


# Signout view handling user logout
# Apply the login_required decorator to ensure that only authenticated users can access this view
@login_required
def signout(request):
    # Log the user out by terminating the session
    logout(request)
    # Redirect the user to the 'home' page
    return redirect('home')


# Signin view handling user login
def signin(request):
    # Check if the request method is GET
    if request.method == 'GET':
        # Render the signin.html template with an instance of the AuthenticationForm
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        # Attempt to authenticate the user using provided username and password
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'])

        # Check if authentication failed
        if user is None:
            # Render the signin.html template with an AuthenticationForm instance and an error message
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })

        # Authentication successful
        else:
            # Log in the user by creating a session
            login(request, user)
            # Redirect to the 'tasks' page
            return redirect('tasks')

