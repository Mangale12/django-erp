from django.db import models


class BillType(models.Model):
    bill_type_name = models.CharField(max_length=256, unique=True, help_text="Name of the bill type")
    description = models.TextField(null=True, blank=True, help_text="Description of the bill type")
    is_active = models.BooleanField(default=True, help_text="Is the bill type active?")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the bill type was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the bill type was last updated")

    class Meta:
        ordering = ["bill_type_name"]
        verbose_name = "Bill Type"
        verbose_name_plural = "Bill Types"

    def __str__(self):
        return self.bill_type_name
