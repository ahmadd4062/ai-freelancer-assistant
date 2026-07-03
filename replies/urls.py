from django.urls import path
from . import views

urlpatterns = [
    path('', views.reply_list, name='reply_list'),
    path('create/', views.reply_create, name='reply_create'),
    path('<int:pk>/', views.reply_detail, name='reply_detail'),
    path('<int:pk>/delete/', views.reply_delete, name='reply_delete'),
    path('<int:pk>/generate/', views.reply_generate, name='reply_generate'),
]