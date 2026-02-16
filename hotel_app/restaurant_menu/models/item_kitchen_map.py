from django.db import models
from .menu_item import MenuItem
from .kitchen import Kitchen
from .kitchen_station import KitchenStation

class ItemKitchenMap(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='kitchen_mappings', help_text="Menu item")
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='item_mappings', help_text="Kitchen")
    kitchen_station = models.ForeignKey(KitchenStation, on_delete=models.CASCADE, related_name='item_mappings', help_text="Kitchen station")
    expected_time = models.IntegerField(help_text="Expected time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('menu_item', 'kitchen', 'kitchen_station')
        verbose_name = "Item Kitchen Map"
        verbose_name_plural = "Item Kitchen Maps"
    
    def __str__(self):
        return f"{self.menu_item.name} -> {self.kitchen.name} -> {self.kitchen_station.name}"
    