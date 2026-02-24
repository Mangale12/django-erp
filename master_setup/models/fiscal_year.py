from django.db import models


class FiscalYear(models.Model):
    fiscal_year_name = models.CharField(
        max_length=256,
        unique=True,
        help_text="Name of the fiscal year",
    )
    start_date = models.DateField(help_text="Start date of fiscal year")
    end_date = models.DateField(help_text="End date of fiscal year")
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the fiscal year",
    )
    is_active = models.BooleanField(default=True, help_text="Is the fiscal year active?")
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the fiscal year was created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the fiscal year was last updated",
    )

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Fiscal Year"
        verbose_name_plural = "Fiscal Years"

    def __str__(self):
        return self.fiscal_year_name
