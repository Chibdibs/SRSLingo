from django.db import models


class Flashcard(models.Model):
    front_text = models.TextField()
    back_text = models.TextField()
    # etc

    def __str__(self):
        return self.front_text[:50]
