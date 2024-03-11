from django.shortcuts import render
from .models import Flashcard


def flashcard_view(request):
    flashcards = Flashcard.objects.all()
    return render(request, 'language_app/flashcards.html', {'flashcards': flashcards})


# def flashcards(request):
#     return render(request, 'language_app/flashcards.html')
