from django import forms
from django.core.exceptions import ValidationError
from hotel_app.reception.models import Booking

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = [
            'guest',
            'booking_source',
            'check_in_date',
            'check_out_date',
            'room',
            'no_of_adults',
            'no_of_children',
            'package_type',
            'discount_type',
            'discount_amount',
            'special_request',
            'booking_status',
            'remarks',
        ]

    def clean(self):
        cleaned_data = super().clean()

        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')

        if check_in and check_out and check_in >= check_out:
            raise ValidationError(
                "Check-out date must be after check-in date."
            )

        return cleaned_data
