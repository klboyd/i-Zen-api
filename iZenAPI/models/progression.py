from django.db import models
from django.contrib.auth.models import User


class Progression(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.ForeignKey(
        User, verbose_name=("user"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "progression"
        verbose_name_plural = "progressions"

    def __str__():
        return f"{self.name} created at {self.created_at}"
