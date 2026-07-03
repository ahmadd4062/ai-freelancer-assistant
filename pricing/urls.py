from django.urls import path
from . import views

urlpatterns = [
    path('', views.pricing_list, name='pricing_list'),
    path('calculator/', views.pricing_calculator, name='pricing_calculator'),
    path('<int:pk>/', views.pricing_detail, name='pricing_detail'),
    path('<int:pk>/delete/', views.pricing_delete, name='pricing_delete'),
]