from django.conf import settings
from django.db import models


class ItemKitchenMap(models.Model):
    map_id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(
        "restaurant_menu.MenuItem",
        on_delete=models.CASCADE,
        related_name="kitchen_mappings",
    )
    kitchen = models.ForeignKey(
        "restaurant_menu.Kitchen",
        on_delete=models.CASCADE,
        related_name="item_mappings",
    )

    class Meta:
        db_table = "mst_item_kitchen_map"
        unique_together = ("item", "kitchen")
        verbose_name = "Item Kitchen Map"
        verbose_name_plural = "Item Kitchen Map"

    def __str__(self):
        return f"{self.item} -> {self.kitchen}"


class KOTHeader(models.Model):
    KOT_TYPE_CHOICES = (
        ("new_order", "New Order"),
        ("running_order", "Running Order"),
        ("void_cancel", "Void/Cancel KOT"),
    )

    kot_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(
        "restaurant_menu.Order",
        on_delete=models.CASCADE,
        related_name="kot_headers",
    )
    kot_number = models.CharField(max_length=64, unique=True)
    kitchen = models.ForeignKey(
        "restaurant_menu.Kitchen",
        on_delete=models.CASCADE,
        related_name="kot_headers",
    )
    waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fired_kots",
    )
    kot_type = models.CharField(max_length=20, choices=KOT_TYPE_CHOICES, default="new_order")
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_printed = models.DateTimeField(null=True, blank=True)
    is_urgent = models.BooleanField(default=False)
    total_items_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "trn_kot_header"
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["kitchen"]),
            models.Index(fields=["timestamp_created"]),
        ]
        verbose_name = "KOT Header"
        verbose_name_plural = "KOT Headers"

    def __str__(self):
        return self.kot_number


class KOTLineItem(models.Model):
    ITEM_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("preparing", "Preparing"),
        ("ready", "Ready"),
        ("bounced", "Bounced"),
        ("served", "Served"),
    )

    kot_line_id = models.BigAutoField(primary_key=True)
    kot = models.ForeignKey(
        "restaurant_menu.KOTHeader",
        on_delete=models.CASCADE,
        related_name="line_items",
    )
    item = models.ForeignKey(
        "restaurant_menu.MenuItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="kot_line_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    modifiers_text = models.TextField(blank=True, help_text="Combined add-ons for chef reference")
    cooking_instruction = models.TextField(
        blank=True,
        help_text='e.g. "Well Done", "Allergy: Nuts"',
    )
    item_status = models.CharField(max_length=20, choices=ITEM_STATUS_CHOICES, default="pending")
    timestamp_start_cooking = models.DateTimeField(null=True, blank=True)
    timestamp_ready = models.DateTimeField(null=True, blank=True)
    chef = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_kot_line_items",
    )

    class Meta:
        db_table = "trn_kot_line_items"
        indexes = [
            models.Index(fields=["kot"]),
            models.Index(fields=["item_status"]),
        ]
        verbose_name = "KOT Line Item"
        verbose_name_plural = "KOT Line Items"

    def __str__(self):
        return f"KOT {self.kot_id} - Line {self.kot_line_id}"


class KDSLog(models.Model):
    ACTION_CHOICES = (
        ("fire", "Fire"),
        ("bump", "Bump"),
        ("recall", "Recall"),
    )

    log_id = models.BigAutoField(primary_key=True)
    kot_line = models.ForeignKey(
        "restaurant_menu.KOTLineItem",
        on_delete=models.CASCADE,
        related_name="kds_logs",
    )
    station_id = models.CharField(max_length=100)
    action_taken = models.CharField(max_length=20, choices=ACTION_CHOICES)
    delay_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "trn_kds_logs"
        indexes = [models.Index(fields=["kot_line", "created_at"])]
        verbose_name = "KDS Log"
        verbose_name_plural = "KDS Logs"

    def __str__(self):
        return f"{self.station_id} - {self.action_taken}"


class KOTAmendment(models.Model):
    ACTION_CHOICES = (
        ("added", "Added"),
        ("cancelled", "Cancelled"),
        ("changed", "Changed"),
    )

    REASON_CODE_CHOICES = (
        ("kitchen_mistake", "Kitchen mistake"),
        ("guest_changed_mind", "Guest changed mind"),
        ("quality_issue", "Quality issue"),
    )

    amendment_id = models.BigAutoField(primary_key=True)
    kot = models.ForeignKey(
        "restaurant_menu.KOTHeader",
        on_delete=models.CASCADE,
        related_name="amendments",
    )
    original_item = models.ForeignKey(
        "restaurant_menu.MenuItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="kot_amendments",
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_kot_amendments",
    )
    reason_code = models.CharField(max_length=30, choices=REASON_CODE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "trn_kot_amendments"
        indexes = [models.Index(fields=["kot", "created_at"])]
        verbose_name = "KOT Amendment"
        verbose_name_plural = "KOT Amendments"

    def __str__(self):
        return f"{self.kot_id} - {self.action}"
