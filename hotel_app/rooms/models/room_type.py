from django.db import models

class RoomType(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text='A short code to identify the room type (max 50 characters)')
    description = models.TextField(blank=True)
    max_adults = models.PositiveIntegerField(default=2)
    max_children = models.PositiveIntegerField(default=0)
    default_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True),
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name
