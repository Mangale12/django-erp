from django.db import models

class MenuCategory(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the menu category (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the menu category (max 256 characters)')
    description = models.TextField(unique=False, null=True, blank=True, help_text='Description of the menu category (max 256 characters)')
    is_active = models.BooleanField(default=True, help_text='Is the menu category active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the menu category was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the menu category was last updated')
    