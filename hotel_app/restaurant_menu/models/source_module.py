from django.db import models


class SourceModule(models.Model):
    module_name = models.CharField(max_length=150, unique=True)
    module_code = models.CharField(max_length=50, unique=True)
    is_postable_to_folio = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Source Module"
        verbose_name_plural = "Source Modules"
        ordering = ["module_name"]

    def __str__(self):
        return f"{self.module_name} ({self.module_code})"
