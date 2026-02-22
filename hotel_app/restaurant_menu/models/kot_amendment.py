from django.conf import settings
from django.db import models
from django.utils import timezone


class KOTAmendment(models.Model):
    ACTION_TYPE_CHOICES = (
        ("ADDED", "Added"),
        ("CANCELLED", "Cancelled"),
        ("QUANTITY_CHANGED", "Quantity Changed"),
        ("ITEM_CHANGED", "Item Changed"),
    )

    amendment_id = models.BigAutoField(primary_key=True, db_column="Amendment_ID")
    business_date = models.DateField(db_column="Business_Date")
    kot = models.ForeignKey(
        "KOTHeader",
        on_delete=models.CASCADE,
        related_name="amendments",
        db_column="KOT_ID",
    )
    kot_line_item = models.ForeignKey(
        "KOTLineItem",
        on_delete=models.SET_NULL,
        related_name="amendments",
        null=True,
        blank=True,
        db_column="KOT_Line_ID",
    )
    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="amendments",
        db_column="Order_ID",
    )
    original_item = models.ForeignKey(
        "MenuItem",
        on_delete=models.CASCADE,
        related_name="original_kot_amendments",
        db_column="Original_Item_ID",
    )
    new_item = models.ForeignKey(
        "MenuItem",
        on_delete=models.SET_NULL,
        related_name="new_kot_amendments",
        null=True,
        blank=True,
        db_column="New_Item_ID",
    )
    action_type = models.CharField(max_length=30, choices=ACTION_TYPE_CHOICES, db_column="Action_Type")
    old_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_column="Old_Quantity")
    new_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_column="New_Quantity")
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="managed_kot_amendments",
        db_column="Manager_ID",
    )
    reason_code = models.CharField(max_length=100, db_column="Reason_Code")
    remarks = models.TextField(null=True, blank=True, db_column="Remarks")
    timestamp_amended = models.DateTimeField(default=timezone.now, db_column="Timestamp_Amended")
    amended_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="amended_kot_amendments",
        db_column="Amended_By",
    )

    class Meta:
        db_table = "trn_kot_amendments"
        verbose_name = "KOT Amendment"
        verbose_name_plural = "KOT Amendments"
        ordering = ["-timestamp_amended", "-amendment_id"]

    def __str__(self):
        return f"{self.amendment_id} | {self.get_action_type_display()}"
 