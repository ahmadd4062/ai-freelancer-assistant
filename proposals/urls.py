from django.urls import path
from . import views

urlpatterns = [
    path('', views.proposal_list, name='proposal_list'),
    path('create/', views.proposal_create, name='proposal_create'),
    path('<int:pk>/', views.proposal_detail, name='proposal_detail'),
    path('<int:pk>/edit/', views.proposal_edit, name='proposal_edit'),
    path('<int:pk>/delete/', views.proposal_delete, name='proposal_delete'),
    path('<int:pk>/generate/', views.proposal_generate, name='proposal_generate'),
    path('<int:pk>/export-pdf/', views.proposal_export_pdf, name='proposal_export_pdf'),
]