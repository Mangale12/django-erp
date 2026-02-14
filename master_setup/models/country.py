# models.py
from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=128, unique=True)
    code = models.CharField(max_length=2, unique=True, help_text="ISO 3166-1 alpha-2 code")
    code_alpha3 = models.CharField(max_length=3, unique=True, help_text="ISO 3166-1 alpha-3 code")
    phone_code = models.CharField(max_length=10, blank=True, help_text="International dialing code (e.g., '1', '44')")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return self.name