from django.db import models


class Kitchen(models.Model):
    KITCHEN_TYPE_CHOICES = (
        ("food", "Food"),
        ("beverage", "Beverage"),
        ("shisha", "Shisha"),
        ("pastry", "Pastry"),
    )

    kitchen_name = models.CharField(
        max_length=256,
        unique=True,
        null=True,
        blank=True,
        help_text="Kitchen name (e.g., Cold Kitchen, Bakery, Bar, Main Galley)",
    )
    kitchen_type = models.CharField(
        max_length=20,
        choices=KITCHEN_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text="Kitchen type",
    )
    printer_ip_address = models.GenericIPAddressField(
        protocol="IPv4",
        null=True,
        blank=True,
        help_text="Network address for thermal printer",
    )
    backup_printer_ip = models.GenericIPAddressField(
        protocol="IPv4",
        null=True,
        blank=True,
        help_text="Failover printer IP address",
    )
    kds_display_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Linked KDS display/tablet identifier",
    )
    is_active = models.BooleanField(default=True, help_text="Is this kitchen active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mst_kitchens"
        verbose_name = "Kitchen"
        verbose_name_plural = "Kitchens"

    def __str__(self):
        return self.kitchen_name
