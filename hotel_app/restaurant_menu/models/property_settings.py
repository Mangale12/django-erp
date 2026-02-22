from django.db import models


class PropertySettings(models.Model):
    property = models.OneToOneField(
        "restaurant_menu.Property",
        on_delete=models.CASCADE,
        related_name="settings",
    )

    enable_kot_module = models.BooleanField(default=False)
    enable_table_management = models.BooleanField(default=False)
    enable_room_module = models.BooleanField(default=False)
    enable_folio_module = models.BooleanField(default=False)
    enable_laundry_module = models.BooleanField(default=False)
    enable_spa_module = models.BooleanField(default=False)
    enable_inventory_module = models.BooleanField(default=False)
    enable_credit_sales = models.BooleanField(default=False)
    enable_multi_outlet = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Property Setting"
        verbose_name_plural = "Property Settings"
        ordering = ["-created_at"]

    def __str__(self):
        property_name = getattr(self.property, "property_name", None) or f"Property {self.property_id}"
        return f"Settings - {property_name}"
