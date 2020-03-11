from django.db import models


class ActionItemStatus(models.Model):
    """
    This class creates the model for ActionItemStatus

    """

    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "action_item_status"
        verbose_name_plural = "action_item_statuses"

    def __str__(self):
        return self.name
