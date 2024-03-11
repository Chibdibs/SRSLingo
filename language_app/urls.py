# language_app/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('flashcards/', views.flashcard_view, name='flashcards'),
    # Add more URLs specific to language learning features
]
