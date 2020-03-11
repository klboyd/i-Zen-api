from django.db import models
from .retro import Retro
from .note_board import NoteBoard


class RetroNoteBoard(models.Model):

    retro = models.ForeignKey(Retro, verbose_name="retro", on_delete=models.CASCADE)
    note_board = models.ForeignKey(
        NoteBoard, verbose_name="note_board", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "retro_note_board"
        verbose_name_plural = "retro_note_boards"

    def __str__(self):
        return self.name
