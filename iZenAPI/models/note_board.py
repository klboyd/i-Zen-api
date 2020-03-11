from django.db import models


class NoteBoard(models.Model):
    """
    This class creates the model for Note Board

    """

    name = models.CharField(max_length=50)
    board_type = models.CharField(max_length=50)

    class Meta:
        verbose_name = "note_board"
        verbose_name_plural = "note_boards"

    def __str__(self):
        return f"{self.name} is {self.type}"
