from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task, FavoriteTask
from .serializers import TaskSerializer, FavoriteTaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteTaskViewSet(viewsets.ModelViewSet):
    queryset = FavoriteTask.objects.all()
    serializer_class = FavoriteTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
