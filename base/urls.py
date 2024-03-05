from django.urls import path
from base import views
from django.contrib.auth import views as auth_views

from base.views import CustomLoginView

urlpatterns = [
    path('', views.landing_page, name='landing'),  # Landing page as the root
    path('home/', views.home, name='home'),  # Home page (displays user dashboard)

    # Authentication views
    path('register/', CustomLoginView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Redirect to landing page on logout
]
