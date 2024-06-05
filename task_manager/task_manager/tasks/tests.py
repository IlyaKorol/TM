from django.test import TestCase, Client
from django.urls import reverse
from .models import Task, FavoriteTask
from .forms import TaskForm, UserRegistrationForm
from django.contrib.auth.models import User


class TaskViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            priority=1,
            due_date='2024-12-31',
            completed=False
        )

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')

    def test_task_detail_view(self):
        response = self.client.get(reverse('task_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')

class TaskViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_task_create_view(self):
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

    def test_task_update_view(self):
        task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            priority=1,
            due_date='2024-12-31',
            completed=False
        )
        response = self.client.get(reverse('task_update', args=[task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            priority=1,
            due_date='2024-12-31',
            completed=False
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.priority, 1)
        self.assertEqual(self.task.due_date, '2024-12-31')
        self.assertFalse(self.task.completed)

class FavoriteTaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            priority=1,
            due_date='2024-12-31',
            completed=False
        )

    def test_favorite_task_creation(self):
        favorite_task = FavoriteTask.objects.create(user=self.user, task=self.task)
        self.assertEqual(favorite_task.user, self.user)
        self.assertEqual(favorite_task.task, self.task)


class TaskFormTest(TestCase):
    def test_task_form_valid_data(self):
        form = TaskForm(data={
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 1,
            'due_date': '2024-12-31',
            'completed': False
        })
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_data(self):
        form = TaskForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)  # Проверяем количество ошибок, ожидаем 4, так как обязательные поля

class UserRegistrationFormTest(TestCase):
    def test_user_registration_form_valid_data(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertTrue(form.is_valid())

    def test_user_registration_form_invalid_data(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)  # Проверяем количество ошибок, ожидаем 3, так как обязательные поля






