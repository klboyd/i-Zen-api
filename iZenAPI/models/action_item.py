from django.db import models
from .action_item_status import ActionItemStatus
from .progression import Progression
from django.contrib.auth.models import User


class ActionItem(models.Model):

    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    due_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    completed_at = models.DateTimeField(auto_now=False, auto_now_add=False, null=True,)
    status = models.ForeignKey(
        ActionItemStatus, verbose_name="action_item_status", on_delete=models.CASCADE
    )
    progression = models.ForeignKey(
        Progression, verbose_name="progression", on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User,
        verbose_name="created_b",
        related_name="created_by",
        on_delete=models.CASCADE,
    )
    completed_by = models.ForeignKey(
        User,
        verbose_name="completed_by",
        related_name="completed_by",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = "action_item"
        verbose_name_plural = "action_items"

    def __str__(self):
        return f"{self.description}"
