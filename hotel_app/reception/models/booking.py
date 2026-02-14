from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Booking(models.Model):

    PACKAGE_TYPE = (
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Family', 'Family'),
    )

    guest = models.ForeignKey('Guest', on_delete=models.CASCADE, related_name='bookings')
    booking_source = models.ForeignKey('master_setup.BookingSource', on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)

    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()

    room = models.ForeignKey('rooms.room', on_delete=models.CASCADE, related_name='bookings')

    no_of_adults = models.IntegerField(default=1, null=True, blank=True)
    no_of_children = models.IntegerField(default=0, null=True, blank=True)

    package_type = models.CharField(
        max_length=256, choices=PACKAGE_TYPE, null=True, blank=True
    )

    discount_type = models.ForeignKey(
        'master_setup.DiscountType', on_delete=models.CASCADE, related_name='bookings', null=True, blank=True
    )
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)

    special_request = models.TextField(null=True, blank=True)
    booking_status = models.CharField(max_length=256, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        errors = {}

        # ✔ Check-in must be before check-out
        if self.check_in_date and self.check_out_date:
            if self.check_in_date >= self.check_out_date:
                errors['check_out_date'] = "Check-out date must be after check-in date."

        # ✔ Check-in cannot be in the past
        if self.check_in_date and self.check_in_date < timezone.now():
            errors['check_in_date'] = "Check-in date cannot be in the past."

        # ✔ Adults must be at least 1
        if self.no_of_adults is not None and self.no_of_adults < 1:
            errors['no_of_adults'] = "At least one adult is required."

        # ✔ Children cannot be negative
        if self.no_of_children is not None and self.no_of_children < 0:
            errors['no_of_children'] = "Number of children cannot be negative."

        # ✔ Discount cannot be negative
        if self.discount_amount < 0:
            errors['discount_amount'] = "Discount amount cannot be negative."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"Booking #{self.id} - {self.guest}"
