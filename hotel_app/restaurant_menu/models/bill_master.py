from django.db import models

# Create your models here.
from master_setup.models.bill_type import BillType

from hotel_app.reception.models import Guest
from hotel_app.rooms.models import Room

class BillMaster(models.Model):
    
    BILL_STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('generated', 'Generated'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('void', 'Void'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
        ('fully_refunded', 'Fully Refunded'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('partially_refunded', 'Partially Refunded'),
        ('fully_refunded', 'Fully Refunded'),
    )
    bill_no = models.CharField(max_length=250, unique=True, null=True, blank=True, help_text="Bill number")
    property = models.ForeignKey('restaurant_menu.Property', on_delete=models.PROTECT, related_name="bill_masters", null=True, blank=True, help_text="Property for the bill")
    outlet = models.ForeignKey('restaurant_menu.Outlet', on_delete=models.PROTECT, related_name="bill_masters", null=True, blank=True, help_text="Outlet for the bill")
    bill_type = models.ForeignKey(BillType, on_delete=models.PROTECT, related_name="bill_masters", null=True, blank=True, help_text="Bill type for the bill")
    source_module = models.ForeignKey('restaurant_menu.SourceModule', on_delete=models.PROTECT, related_name="bill_masters", null=True, blank=True, help_text="Source module for the bill")
    order = models.ForeignKey('restaurant_menu.Order', on_delete=models.PROTECT, related_name="bill_masters", null=True, blank=True, help_text="Order for the bill")
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT, related_name="bill_masters", null=True, blank=True, help_text="Guest for the bill")
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="bill_masters", null=True, blank=True, help_text="Room for the bill")
    stay = models.ForeignKey('reception.Stay', on_delete=models.PROTECT, related_name="bill_masters", null=True, blank=True, help_text="Stay for the bill")
    folio = models.ForeignKey('restaurant_menu.Folio', on_delete=models.PROTECT, related_name="bill_masters", null=True, blank=True, help_text="Folio for the bill")
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Sub total for the bill")
    discount_type = models.ForeignKey('master_setup.DiscountType', on_delete=models.PROTECT, related_name="bill_masters", null=True, blank=True, help_text="Discount type for the bill")
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Discount value for the bill")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Discount amount for the bill")
    extra_charge_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Extra charge amount for the bill")
    service_charge_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Service charge amount for the bill")
    tax_type = models.ForeignKey('master_setup.TaxType', on_delete=models.PROTECT, related_name="bill_masters", null=True, blank=True, help_text="Tax type for the bill")
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Tax amount for the bill")
    round_off = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Round off for the bill")
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Grand total for the bill")
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='pending', help_text="Payment status for the bill")
    bill_status = models.CharField(max_length=50, choices=BILL_STATUS_CHOICES, default='draft', help_text="Bill status for the bill")
    created_by = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name="bill_masters", null=True, blank=True, help_text="Created by for the bill")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the bill was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the bill was last updated")
    
    
    def __str__(self):
        return self.bill_no or f"Bill-{self.pk or 'N/A'}"
    
    class Meta:
        verbose_name = "Bill Master"
        verbose_name_plural = "Bill Masters"
        ordering = ["-created_at"]
        
class BillLineItem(models.Model):
    bill_master = models.ForeignKey(BillMaster, on_delete=models.PROTECT, related_name="bill_line_items", null=True, blank=True, help_text="Bill master for the bill line item")
    item = models.ForeignKey('restaurant_menu.MenuItem', on_delete=models.PROTECT, related_name="bill_line_items", null=True, blank=True, help_text="Item for the bill line item")
    item_name_snapshot = models.TextField(null=True, blank=True, help_text="Item name snapshot for the bill line item")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Quantity for the bill line item")
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Rate for the bill line item")
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Amount for the bill line item")
    discount_type = models.ForeignKey('master_setup.DiscountType', on_delete=models.PROTECT, related_name="bill_line_items", null=True, blank=True, help_text="Discount type for the bill line item")
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Discount value for the bill line item")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Discount amount for the bill line item")
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Net amount for the bill line item")
    is_complementary = models.BooleanField(default=False, help_text="Is the bill line item a complementary item?")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the bill line item was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the bill line item was last updated")
    
    def __str__(self):
        return self.item_name_snapshot or (self.item.name if self.item else f"Line-{self.pk}")
