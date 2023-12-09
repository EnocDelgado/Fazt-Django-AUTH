from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse # to create a page and see it on browser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User # Create a Database Model for us
from django.contrib.auth import login, logout, authenticate # Create Cookie
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render( request, 'home.html')


def signup(request):

    # validation
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Create user based data provided from the form signup
                user = User.objects.create_user(username=request.POST['username'], 
                                        password=request.POST['password1'])
                
                # save in databae
                user.save()
                # Create cookie
                login(request, user)
                # redirect page
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


@login_required
def tasks(request):
    # get all tasks
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)

    return render( request, 'tasks.html', { 'tasks': tasks })


@login_required
def tasks_completed(request):
    # get all tasks
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')

    return render( request, 'tasks.html', { 'tasks': tasks })


@login_required
def create_task(request):

    # validation
    if request.method == 'GET':
        return render( request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            # get information from form
            form = TaskForm(request.POST)

            new_task = form.save(commit=False)

            # save data in database
            new_task.user = request.user
            new_task.save()

            # display our data
            return redirect('tasks')

        except ValueError:

            return render(request, 'create_tasks.html', {
                'form': TaskForm,
                'error': 'Please provide validate data'
            })


@login_required
def task_detail(request, task_id):

    # validation
    if request.method == 'GET':
        # get_object_or_404 allows to avoid our server down
        task = get_object_or_404(Task, pk=task_id, user=request.user) 

        # Display form when user wants edit their task
        form = TaskForm(instance=task)

        return render(request, 'task_detail.html', { 'task': task, 'form': form })

    else:
        try:
            # get_object_or_404 allows to avoid our server down
            task = get_object_or_404(Task, pk=task_id, user=request.user) 
            # invoke taksForm to recive data from form
            form = TaskForm(request.POST, instance=task)
            # Save in database
            form.save()

            return redirect('tasks')
        
        except ValueError:
            return render( request, 'task_detail.html', { 
                'task': task,
                'form': form,
                'error': "Error updating task"
             })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def signout(request):
    logout(request)
    return redirect('home')



def signin(request):

    # validation
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        
        user = authenticate(
            request, 
            username=request.POST['username'], 
            password=request.POST['password'])
        
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        
        else:
            login(request, user)
            return redirect('tasks')