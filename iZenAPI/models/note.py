from django.db import models
from .retro_note_board import RetroNoteBoard
from django.contrib.auth.models import User


class Note(models.Model):

    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    retro_note_board = models.ForeignKey(
        RetroNoteBoard, verbose_name="retro_note_board", on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "note"
        verbose_name_plural = "notes"

    def __str__(self):
        return self.description
