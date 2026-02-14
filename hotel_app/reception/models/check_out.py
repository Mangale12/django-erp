from django.conf import settings
import django.db.models as models

class CheckOut(models.Model):
    guest = models.ForeignKey('Guest', on_delete=models.CASCADE, related_name='check_outs')
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='check_outs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='check_outs', null=True, blank=True)
    check_in = models.ForeignKey('CheckIn', on_delete=models.CASCADE, related_name='check_outs', null=True, blank=True)
    check_out_time = models.DateTimeField(auto_now_add=True, help_text='Date and time when the guest checked out', editable=True)
    late_check_out_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Late check-out charge')
    minibar_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Minibar charge')
    damage_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Damage charge')
    other_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Other charge')
    final_bill_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Final bill amount')
    payment_mode = models.ForeignKey('master_setup.PaymentMode', on_delete=models.CASCADE, related_name='check_outs')
    remarks = models.TextField(unique=False, null=True, blank=True, help_text='Remarks of the check-out (max 256 characters)')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the check-out was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the check-out was last updated')
    

    def __str__(self):
        return f"{self.check_in} - {self.guest}"
    
    class Meta:
        verbose_name = 'Check Out'
        verbose_name_plural = 'Check Outs'
        ordering = ['-check_out_time']