from django.db import models
from .progression import Progression
from django.contrib.auth.models import User


class Retro(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    progression = models.ForeignKey(
        Progression, verbose_name="progression", on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "retro"
        verbose_name_plural = "retros"

    def __str__(self):
        return f"{self.name} for progression {self.progression}"
