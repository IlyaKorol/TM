from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, FavoriteTask

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class FavoriteTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteTask
        fields = '__all__'
