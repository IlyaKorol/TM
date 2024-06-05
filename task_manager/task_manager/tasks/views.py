from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from .forms import UserRegistrationForm, TaskForm
from django.contrib.auth.decorators import login_required
from .models import Task, FavoriteTask
from django.db.models import Q
from django.contrib.auth import logout as auth_logout
import logging


logger = logging.getLogger(__name__)

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('task_list')


@login_required
def task_list(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        completed = request.POST.get('completed') == 'on'
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.completed = completed
        task.save()
        return redirect('task_list')

    tab = request.GET.get('tab', 'all')
    query = request.GET.get('q')
    order_by = request.GET.get('order_by', 'title')
    order_direction = request.GET.get('order_direction', 'asc')

    all_tasks = Task.objects.filter(user=request.user)

    if query:
        all_tasks = all_tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

    next_direction = 'desc' if order_direction == 'asc' else 'asc'

    order_by_prefix = '' if order_direction == 'asc' else '-'
    if order_by in ['title', 'priority', 'due_date', 'created_at']:
        all_tasks = all_tasks.order_by(f'{order_by_prefix}{order_by}')

    if tab == 'completed':
        tasks = all_tasks.filter(completed=True)
    elif tab == 'favorite':
        tasks = all_tasks.filter(favorited_by__user=request.user)
        if order_by in ['title', 'priority', 'due_date', 'created_at']:
            tasks = tasks.order_by(f'{order_by_prefix}{order_by}')
    else:
        tasks = all_tasks.exclude(completed=True)


    completed_tasks = all_tasks.filter(completed=True)
    all_tasks = all_tasks.exclude(completed=True)
    favorite_tasks = Task.objects.filter(favorited_by__user=request.user)
    if order_by in ['title', 'priority', 'due_date', 'created_at']:
        favorite_tasks = favorite_tasks.order_by(f'{order_by_prefix}{order_by}')

    return render(request, 'tasks/task_list.html', {
        'all_tasks': all_tasks,
        'completed_tasks': completed_tasks,
        'favorite_tasks': favorite_tasks,
        'order_by': order_by,
        'order_direction': order_direction,
        'next_direction': next_direction,
        'tab': tab,
    })


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.completed = request.POST.get('completed') == 'on'
        task.save()
        return redirect('task_list')
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Сохранение задачи, если форма валидна
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            # Перенаправление на страницу списка задач после успешного создания
            return redirect('task_list')
    else:
        # Если метод запроса не POST, отобразить пустую форму для создания задачи
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def add_to_favorite(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    favorite_task, created = FavoriteTask.objects.get_or_create(user=request.user, task=task)
    if created:
        logger.info(f"Task '{task.title}' added to favorites for user '{request.user.username}'.")
    else:
        logger.info(f"Task '{task.title}' is already in favorites for user '{request.user.username}'.")
    return redirect('task_list')


@login_required
def remove_from_favorite(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    FavoriteTask.objects.filter(user=request.user, task=task).delete()
    return redirect('task_list')

@login_required
def favorite_task_list(request):
    favorite_tasks = FavoriteTask.objects.filter(user=request.user)
    return render(request, 'tasks/favorite_task_list.html', {'favorite_tasks': favorite_tasks})

@login_required
def search_tasks(request):
    query = request.GET.get('q')
    tasks = Task.objects.filter(user=request.user).filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'tasks/task_list.html', {'tasks': tasks})