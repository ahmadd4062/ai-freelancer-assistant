from django.urls import path
from . import views

urlpatterns = [
    path('', views.gig_list, name='gig_list'),
    path('create/', views.gig_create, name='gig_create'),
    path('<int:pk>/', views.gig_detail, name='gig_detail'),
    path('<int:pk>/edit/', views.gig_edit, name='gig_edit'),
    path('<int:pk>/delete/', views.gig_delete, name='gig_delete'),
    path('<int:pk>/generate/', views.gig_generate, name='gig_generate'),
]