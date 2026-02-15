from django.db import models
class Outlet(models.Model):
    
    OUTLET_TYPE_CHOICES = (
        ("RESTAURANT", "Restaurant"),
        ("BAR", "Bar"),
        ("LOUNGE", "Lounge"),
        ("ROOM_SERVICE", "Room Service"),
        ("BANQUET", "Banquet"),
        ("CAFE", "Café"),
        ("NIGHT_CLUB", "Night Club"),
    )

    outlet_code = models.CharField(max_length=20, unique=True)
    outlet_name = models.CharField(max_length=150)
    
    outlet_type = models.CharField(
        max_length=20,
        choices=OUTLET_TYPE_CHOICES,
        default="RESTAURANT"
    )

    location_description = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    business_day_start_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Time when business date starts (e.g., 06:00 AM)"
    )

    service_charge_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    vat_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    is_table_service = models.BooleanField(default=True)
    is_buffet_enabled = models.BooleanField(default=False)
    is_kds_enabled = models.BooleanField(default=True)

    allow_order_transfer = models.BooleanField(default=True)
    allow_backdated_orders = models.BooleanField(default=False)
    allow_item_cancel_after_print = models.BooleanField(default=False)
    require_manager_approval_for_void = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mst_outlets"
        verbose_name = "Outlet"
        verbose_name_plural = "Outlets"
        ordering = ["outlet_name"]

    def __str__(self):
        return f"{self.outlet_code} - {self.outlet_name}"
