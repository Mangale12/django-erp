from django.db import models


class KOTLineItem(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PREPARING", "Preparing"),
        ("READY", "Ready"),
        ("BOUNCED", "Bounced"),
        ("SERVED", "Served"),
        ("CANCELLED", "Cancelled"),
    )

    PRIORITY_CHOICES = (
        ("NORMAL", "Normal"),
        ("VIP", "VIP"),
        ("VVIP", "VVIP"),
        ("STAFF", "Staff"),
        ("COMPLIMENTARY", "Complimentary"),
    )

    kot = models.ForeignKey("KOTHeader", on_delete=models.CASCADE, related_name="kot_line_items", help_text="KOT for the KOT line item")
    item = models.ForeignKey("MenuItem", on_delete=models.PROTECT, blank=True, null=True, related_name="kot_line_items", help_text="Item for the KOT line item")
    item_code = models.CharField(max_length=50, blank=True, null=True, help_text="Item code for the KOT line item")
    item_name_snapshot = models.CharField(max_length=255, blank=True, null=True, help_text="Item name snapshot for the KOT line item")
    course_number = models.PositiveIntegerField(default=1, help_text="Course number for the KOT line item")
    fire_sequence = models.PositiveIntegerField(default=1, help_text="Fire sequence for the KOT line item")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity for the KOT line item")
    uom = models.CharField(max_length=50, help_text="Unit of measure for the KOT line item")
    modifiers_text = models.TextField(null=True, blank=True, help_text="Modifiers text for the KOT line item")
    cooking_instruction = models.TextField(null=True, blank=True, help_text="Cooking instruction for the KOT line item")
    allergy_notes = models.TextField(null=True, blank=True, help_text="Allergy notes for the KOT line item")
    is_complimentary = models.BooleanField(default=False)
    item_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    priority_level = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="NORMAL")
    expected_prep_time_minutes = models.PositiveIntegerField(default=0, help_text="Expected prep time minutes for the KOT line item")
    timestamp_fired = models.DateTimeField(null=True, blank=True, help_text="Timestamp fired for the KOT line item")
    timestamp_start_cooking = models.DateTimeField(null=True, blank=True, help_text="Timestamp start cooking for the KOT line item")
    timestamp_ready = models.DateTimeField(null=True, blank=True, help_text="Timestamp ready for the KOT line item")
    timestamp_served = models.DateTimeField(null=True, blank=True, help_text="Timestamp served for the KOT line item")
    timestamp_cancelled = models.DateTimeField(null=True, blank=True)
    chef = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="prepared_kot_items", db_column="Chef_ID")
    station = models.ForeignKey("KitchenStation", on_delete=models.SET_NULL, null=True, blank=True, db_column="Station_ID")
    is_bounced = models.BooleanField(default=False)
    bounce_reason = models.TextField(null=True, blank=True)
    cancelled_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="cancelled_kot_items")
    cancel_approved_by_manager = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_cancel_kot_items", db_column="Cancel_Approved_By_Manager_ID")
    cancellation_reason_code = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "trn_kot_line_items"
        verbose_name = "KOT Line Item"
        verbose_name_plural = "KOT Line Items"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.item_name_snapshot} ({self.quantity})"
