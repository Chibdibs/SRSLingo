import json

from django.shortcuts import render
from .models import Flashcard


def flashcard_view(request):
    flashcards = Flashcard.objects.all()
    flashcards_json = json.dumps(list(flashcards.values('front_text', 'back_text')))
    return render(request, 'language_app/flashcards.html', {'flashcards_json': flashcards_json})

