from django.db import models
from master_setup.models import ShiftType, PriorityLevel
from hotel_app.restaurant_menu.models import Order, KOTType, KOTStatus, Kitchen, Outlet, TableSetup
from hotel_app.reception.models import Guest
from hotel_app.rooms.models import Room

class KOTHeader(models.Model):
    business_date = models.DateField(null=True, blank=True, help_text="Business date for the KOT")
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Outlet for the KOT")
    shift_type = models.ForeignKey(ShiftType, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Shift type for the KOT")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Order for the KOT")
    table = models.ForeignKey(TableSetup, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Table for the KOT")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Room for the KOT")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Guest for the KOT")
    kot_number = models.CharField(max_length=250, null=True, blank=True, help_text="KOT number")
    kitchen = models.ForeignKey('Kitchen', on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Kitchen for the KOT")
    
    # FIXED: Unique related_name for User model to prevent clashes
    waiter = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers_waiter', null=True, blank=True, help_text="Waiter for the KOT")
    captain = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers_captain', null=True, blank=True, help_text="Captain for the KOT")
    
    cover_count = models.IntegerField(null=True, blank=True, help_text="Cover count for the KOT")
    kot_type = models.ForeignKey(KOTType, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="KOT type for the KOT")
    kot_status = models.ForeignKey(KOTStatus, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="KOT status for the KOT")
    priority_level = models.ForeignKey(PriorityLevel, on_delete=models.CASCADE, related_name='kot_headers', null=True, blank=True, help_text="Priority level for the KOT")
    is_urgent = models.BooleanField(default=False, help_text="Is urgent for the KOT")
    is_reprint = models.BooleanField(default=False, help_text="Is reprint for the KOT")
    reprint_count = models.IntegerField(default=0, help_text="Reprint count for the KOT")
    
    # FIXED: Consistent related_name
    printed_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers_printed_by', null=True, blank=True, help_text="User who printed the KOT")
    printed_at = models.DateTimeField(null=True, blank=True, help_text="Printed at for the KOT")
    completed_at = models.DateTimeField(null=True, blank=True, help_text="Completed at for the KOT")
    total_item_count = models.IntegerField(null=True, blank=True, help_text="Total item count for the KOT")
    total_quantity = models.IntegerField(null=True, blank=True, help_text="Total quantity for the KOT")
    is_stock_posted = models.BooleanField(default=False, help_text="Is stock posted for the KOT")
    stock_posted_at = models.DateTimeField(null=True, blank=True, help_text="Stock posted at for the KOT")
    
    # FIXED: Typo in field name (tansfer -> transfer) and unique related_names for Kitchen
    transfer_from_kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kot_headers_transferred_from', null=True, blank=True, help_text="Transfer from kitchen for the KOT")
    transfer_to_kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kot_headers_transferred_to', null=True, blank=True, help_text="Transfer to kitchen for the KOT")
    transfer_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers_transferred_by', null=True, blank=True, help_text="User who transferred the KOT")
    transfer_at = models.DateTimeField(null=True, blank=True, help_text="Transfer at for the KOT")
    
    # FIXED: Consistent related_name
    cancelled_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers_cancelled_by', null=True, blank=True, help_text="User who cancelled the KOT")
    cancelled_at = models.DateTimeField(null=True, blank=True, help_text="Cancelled at for the KOT")
    cancelation_reason = models.TextField(null=True, blank=True, help_text="Cancelation reason for the KOT")
    
    # IMPROVED: Standard naming conventions (create_by -> created_by) and unique related_names
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers_created_by', null=True, blank=True, help_text="User who created the KOT")
    create_at = models.DateTimeField(auto_now_add=True, help_text="Create at for the KOT")
    updated_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_headers_updated_by', null=True, blank=True, help_text="User who updated the KOT")
    update_at = models.DateTimeField(auto_now=True, help_text="Update at for the KOT")

    def __str__(self):
        return f"KOT {self.kot_number} - {self.outlet}"