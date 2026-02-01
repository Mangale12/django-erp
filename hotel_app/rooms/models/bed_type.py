from django.db import models

class BedType(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the bed type (max 256 characters)')
    code = models.CharField(max_length=250, unique=True, null=True, blank=True, help_text='A short code to identify the bed type (max 50 characters)')
    description = models.TextField(blank=True, help_text='Description of the bed type')
    is_active = models.BooleanField(default=True, help_text='Is the bed type active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the bed type was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the bed type was last updated')

    def __str__(self):
        return self.name
