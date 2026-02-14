from django.db import models


class Zone(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the zone (max 256 characters)')
    description = models.TextField(null=True, blank=True, help_text='Description of the zone')
    service_charge_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text='Service charge percentage')
    is_active = models.BooleanField(default=True, help_text='Is the zone active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the zone was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the zone was last updated')

    def __str__(self):
        return self.name