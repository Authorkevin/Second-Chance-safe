from django.urls import path
from . import views

app_name = 'donate'  # Namespace for the app

urlpatterns = [
    path('', views.donation_form_view, name='donate_form'),
    path('success/', views.donation_success_view, name='donation_success'),
    path('cancel/', views.donation_cancel_view, name='donation_cancel'),
]

