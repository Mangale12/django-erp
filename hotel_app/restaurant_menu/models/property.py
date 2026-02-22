from django.db import models


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ("CAFE", "Cafe"),
        ("CANTEEN", "Canteen"),
        ("RESTAURANT", "Restaurant"),
        ("HOTEL", "Hotel"),
        ("RESORT", "Resort"),
        ("MULTI_OUTLET_CHAIN", "Multi-outlet Chain"),
    )

    property_code = models.CharField(max_length=30, unique=True, null=True, blank=True, help_text="Property code")
    property_name = models.CharField(max_length=150, unique=True, null=True, blank=True, help_text="Property name")
    property_type = models.CharField(
        max_length=25,
        choices=PROPERTY_TYPE_CHOICES,
        default="RESTAURANT",
        help_text="Property type",
    )

    address = models.TextField(blank=True, null=True, help_text="Property address")
    city = models.CharField(max_length=250, help_text="City name", null=True, blank=True)
    state = models.CharField(max_length=250, help_text="State name", null=True, blank=True)
    country = models.CharField(max_length=250, help_text="Country name", null=True, blank=True)
    postal_code = models.CharField(max_length=250, null=True, blank=True, help_text="Postal code")

    phone = models.CharField(max_length=250, null=True, blank=True, help_text="Phone number")
    email = models.EmailField(blank=True, null=True, help_text="Email address")
    currency = models.CharField(max_length=250, null=True, blank=True, help_text="Currency")
    website = models.URLField(null=True, blank=True)
    parent_property = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="child_properties",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ["property_name"]

    def __str__(self):
        return f"{self.property_code} - {self.property_name}"
