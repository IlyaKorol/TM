from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/new/', views.task_create, name='task_create'),
    path('task/<int:pk>/edit/', views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('favorites/', views.favorite_task_list, name='favorite_task_list'),
    path('search/', views.search_tasks, name='search_tasks'),
    path('task/<int:pk>/add_to_favorite/', views.add_to_favorite, name='add_to_favorite'),
    path('task/<int:pk>/remove_from_favorite/', views.remove_from_favorite, name='remove_from_favorite'),
]