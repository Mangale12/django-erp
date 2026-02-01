from django.db import models

class RoomViewType(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the room category (max 256 characters)')
    code = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text='A short code to identify the room category (max 50 characters)')
    description = models.TextField(blank=True, help_text='Description of the room category')
    is_active = models.BooleanField(default=True, help_text='Is the room category active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the room category was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the room category was last updated')

    def __str__(self):
        return self.name
