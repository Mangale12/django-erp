from django.db import models


class Modifier(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, help_text="Name of the modifier")
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Extra price of the modifier")
    description = models.TextField(null=True, blank=True, help_text="Description of the modifier")
    is_active = models.BooleanField(default=True, help_text="Is the modifier active?")
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE, null=True, blank=True, help_text="Menu item to which the modifier belongs")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the modifier was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the modifier was last updated")
    

    def __str__(self):
        return self.name
    
    