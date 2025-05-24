from django.urls import path
from . import views

app_name = 'volunteer'

urlpatterns = [
    path('', views.volunteer_signup_view, name='volunteer_signup'),
    path('thank-you/', views.volunteer_thank_you_view, name='volunteer_thank_you'),
]
