from django.urls import path
from . import views

urlpatterns = [
    path('', views.coverletter_list, name='coverletter_list'),
    path('create/', views.coverletter_create, name='coverletter_create'),
    path('<int:pk>/', views.coverletter_detail, name='coverletter_detail'),
    path('<int:pk>/edit/', views.coverletter_edit, name='coverletter_edit'),
    path('<int:pk>/delete/', views.coverletter_delete, name='coverletter_delete'),
    path('<int:pk>/generate/', views.coverletter_generate, name='coverletter_generate'),
]