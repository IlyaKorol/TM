from django.contrib.auth.forms import UserCreationForm
from .models import User, Task
from django import forms

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'completed']
        widgets = {
            'user': forms.HiddenInput(),
            'priority': forms.Select(choices=Task.PRIORITY_CHOICES)
        }