from django.urls import path

from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.Register.as_view(), name='register'),

    path('', views.index.as_view(), name='index'),

    path('details/<pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('new/', views.TaskCreate.as_view(), name='task-add'),
    path('update/<pk>/', views.TaskUpdate.as_view(), name='task-update'),
    path('delete/<pk>/', views.TaskDelete.as_view(), name='task-delete'),
]
