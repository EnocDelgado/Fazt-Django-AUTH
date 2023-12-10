from django.contrib import admin
from django.urls import path
from tasks import views

# Define the urlpatterns list containing various paths and their associated views
urlpatterns = [
    # Path for the home page, mapped to the 'home' view
    path('', views.home, name='home'),

    # Path for user registration, mapped to the 'signup' view
    path('signup/', views.signup, name='signup'),

    # Path for displaying tasks, mapped to the 'tasks' view
    path('tasks/', views.tasks, name='tasks'),

    # Path for displaying completed tasks, mapped to the 'tasks_completed' view
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),

    # Path for creating a new task, mapped to the 'create_task' view
    path('create_task/', views.create_task, name='create_task'),

    # Path for displaying details of a specific task, mapped to the 'task_detail' view
    path('tasks/<int:task_id>', views.task_detail, name='task_detail'),

    # Path for marking a task as completed, mapped to the 'complete_task' view
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),

    # Path for deleting a task, mapped to the 'delete_task' view
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),

    # Path for user logout, mapped to the 'signout' view
    path('logout/', views.signout, name='signout'),

    # Path for user login, mapped to the 'signin' view
    path('signin/', views.signin, name='signin'),
]
