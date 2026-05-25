from django.contrib import admin
from django.urls import path
from boards import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tasks/', views.task_list, name='task_list'),
    path('task/add/', views.task_add, name='task_add'),
    path('board/<int:id>/', views.board_page, name='board'),
    path('task/<int:id>/', views.task_page, name='task'),
    path('task/<int:id>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:id>/delete/', views.task_delete, name='task_delete'),
]
