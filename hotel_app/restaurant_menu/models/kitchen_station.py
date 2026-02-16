from django.db import models
from .kitchen import Kitchen
from master_setup.models import Printer

class KitchenStation(models.Model):
    kitchen = models.ForeignKey(Kitchen, related_name='stations', on_delete=models.CASCADE, null=True, blank=True, help_text="Optional: Assign this station to a specific kitchen")
    name = models.CharField(max_length=255, help_text="Name of the kitchen station")
    printer = models.ForeignKey(Printer, related_name='stations', on_delete=models.SET_NULL, null=True, blank=True, help_text="Optional: Assign this station to a specific printer")
    kds_display_id = models.CharField(max_length=250, blank=True, null=True, help_text="KDS display ID for this station")
    is_active = models.BooleanField(default=True, help_text="Whether this station is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
