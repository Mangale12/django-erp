from django.db import models

class Floor(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the floor (max 256 characters)')
    code = models.CharField(max_length=250, unique=True, null=True, blank=True, help_text='A short code to identify the floor (max 50 characters)')
    description = models.TextField(blank=True, help_text='Description of the floor')
    is_active = models.BooleanField(default=True, help_text='Is the floor active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the floor was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the floor was last updated')

    def __str__(self):
        return self.name
