from django.db import models
from django.conf import settings
from .kitchen_type import KitchenType
from .outlet import Outlet

class Kitchen(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    type = models.ForeignKey(KitchenType, on_delete=models.PROTECT, related_name="kitchens", null=True, blank=True)
    outlet = models.ForeignKey(Outlet, on_delete=models.PROTECT, related_name="kitchens", null=True, blank=True)
    printer_ip_address = models.GenericIPAddressField(null=True, blank=True)
    backup_printer_ip = models.GenericIPAddressField(null=True, blank=True)
    kds_display_id = models.CharField(max_length=50, null=True, blank=True)

    is_kds_enabled = models.BooleanField(default=False)
    is_printer_enabled = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="kitchens_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="kitchens_updated",
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mst_kitchens"
        ordering = ["display_order", "name"]

    def __str__(self):
        return f"{self.code} - {self.name}"
