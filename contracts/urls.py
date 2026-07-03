from django.urls import path
from . import views

urlpatterns = [
    path('', views.contract_list, name='contract_list'),
    path('create/', views.contract_create, name='contract_create'),
    path('<int:pk>/', views.contract_detail, name='contract_detail'),
    path('<int:pk>/edit/', views.contract_edit, name='contract_edit'),
    path('<int:pk>/delete/', views.contract_delete, name='contract_delete'),
    path('<int:pk>/generate/', views.contract_generate, name='contract_generate'),
    path('<int:pk>/pdf/', views.contract_pdf, name='contract_pdf'),
]