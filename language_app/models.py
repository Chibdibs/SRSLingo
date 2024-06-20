from django.db import models


class Flashcard(models.Model):
    front_text = models.CharField(max_length=255)
    back_text = models.CharField(max_length=255)
    # Consider adding more fields like user ownership, timestamps, categories, etc.

    def __str__(self):
        return self.front_text[:50]
# sdfsfsdffs
# sdfsfsdffs
