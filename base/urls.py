from django.urls import path
from base import views


urlpatterns = [
    path('', views.landing_page, name='landing'),  # Landing page as the root
    path('home/', views.home, name='home'),  # Home page, make sure the view exists
    path('register/', views.register, name='register'),
]
