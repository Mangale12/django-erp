from django.db import models
from hotel_app.models import Outlet
from master_setup.models import ShiftType
from restaurant_menu.models.order import Order
from restaurant_menu.models import Table, Room, KOTType, KOTStatus, PriorityLevel, Kitchen
from guest_app.models import Guest

class KOTHeader(models.Model):
    business_date = models.DateField(null=True, blank=True, help_text="Business date for the KOT")
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Outlet for the KOT")
    shift_type = models.ForeignKey(ShiftType, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Shift type for the KOT")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Order for the KOT")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Table for the KOT")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Room for the KOT")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Guest for the KOT")
    kot_number = models.CharField(max_length=250, null=True, blank=True, help_text="KOT number")
    kitchen = models.ForeignKey('Kitchen', on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Kitchen for the KOT")
    waiter = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Waiter for the KOT")
    captain = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Captain for the KOT")
    cover_count = models.IntegerField(null=True, blank=True, help_text="Cover count for the KOT")
    kot_type = models.ForeignKey(KOTType, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="KOT type for the KOT")
    kot_status = models.ForeignKey(KOTStatus, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="KOT status for the KOT")
    priority_level = models.ForeignKey(PriorityLevel, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Priority level for the KOT")
    is_urgent = models.BooleanField(default=False, help_text="Is urgent for the KOT")
    is_reprint = models.BooleanField(default=False, help_text="Is reprint for the KOT")
    reprint_count = models.IntegerField(default=0, help_text="Reprint count for the KOT")
    printed_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers_printed', null=True, blank=True, help_text="User who printed the KOT")
    printed_at = models.DateTimeField(null=True, blank=True, help_text="Printed at for the KOT")
    completed_at = models.DateTimeField(null=True, blank=True, help_text="Completed at for the KOT")
    total_item_count = models.IntegerField(null=True, blank=True, help_text="Total item count for the KOT")
    total_quantity = models.IntegerField(null=True, blank=True, help_text="Total quantity for the KOT")
    is_stock_posted = models.BooleanField(default=False, help_text="Is stock posted for the KOT")
    stock_posted_at = models.DateTimeField(null=True, blank=True, help_text="Stock posted at for the KOT")
    transfer_from_kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kot_headers_transferred', null=True, blank=True, help_text="Transfer from kitchen for the KOT")
    tansfer_to_kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kot_headers_transferred_to', null=True, blank=True, help_text="Transfer to kitchen for the KOT")
    transfer_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers_transferred_by', null=True, blank=True, help_text="User who transferred the KOT")
    transfer_at = models.DateTimeField(null=True, blank=True, help_text="Transfer at for the KOT")
    cancelled_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers_cancelled_by', null=True, blank=True, help_text="User who cancelled the KOT")
    cancelled_at = models.DateTimeField(null=True, blank=True, help_text="Cancelled at for the KOT")
    cancelation_reason = models.TextField(null=True, blank=True, help_text="Cancelation reason for the KOT")
    create_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers_create_by', null=True, blank=True, help_text="User who created the KOT")
    create_at = models.DateTimeField(auto_now_add=True, help_text="Create at for the KOT")
    update_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers_update_by', null=True, blank=True, help_text="User who updated the KOT")
    update_at = models.DateTimeField(auto_now=True, help_text="Update at for the KOT")