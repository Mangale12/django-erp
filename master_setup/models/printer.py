from django.db import models


class Printer(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the printer (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the printer (max 256 characters)')
    printer_type = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Printer type (max 256 characters)')
    ip_address = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='IP address of the printer (max 256 characters)')
    port = models.IntegerField(unique=True, null=True, blank=True, help_text='Port of the printer (max 256 characters)')
    
    description = models.TextField(unique=False, null=True, blank=True, help_text='Description of the printer (max 256 characters)')
    is_active = models.BooleanField(default=True, help_text='Is the printer active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the printer was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the printer was last updated')
    