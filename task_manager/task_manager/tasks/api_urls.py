from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import TaskViewSet, FavoriteTaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'favorite-tasks', FavoriteTaskViewSet, basename='favorite-task')

urlpatterns = [
    path('', include(router.urls)),
]
