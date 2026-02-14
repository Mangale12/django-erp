from django.db import models
from django.conf import settings

class CheckIn(models.Model):
    booking = models.ForeignKey(
        'Booking',
        on_delete=models.CASCADE,
        related_name='check_ins'
    )

    guest = models.ForeignKey(
        'Guest',
        on_delete=models.CASCADE,
        related_name='check_ins'
    )

    room = models.ForeignKey(
        'rooms.Room',
        on_delete=models.CASCADE,
        related_name='check_ins'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='check_ins'
    )

    payment_mode = models.ForeignKey(
        'master_setup.PaymentMode',
        on_delete=models.CASCADE,
        related_name='check_ins'
    )

    advance_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    remarks = models.TextField(null=True, blank=True)

    check_in_time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
