from django import forms
from django.core.exceptions import ValidationError
from hotel_app.reception.models import CheckIn, CheckOut

class CheckOutForm(forms.ModelForm):

    class Meta:
        model = CheckOut
        fields = [
            'guest',
            'room',
            'user',
            'check_in',
            'late_check_out_charge',
            'minibar_charge',
            'damage_charge',
            'other_charge',
            'final_bill_amount',
            'payment_mode',
            'remarks',
        ]

    def clean_check_in(self):
        check_in = self.cleaned_data.get('check_in')
        if check_in is None:
            raise ValidationError("Check-in is required.")
        return check_in

    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        room = cleaned_data.get('room')

        if check_in and room:
            if check_in.room != room:
                raise ValidationError(
                    "Selected room does not match the check-in room."
                )

        return cleaned_data

    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        booking = cleaned_data.get('booking')
        room = cleaned_data.get('room')

        if booking and room:
            if booking.room != room:
                raise ValidationError(
                    "Selected room does not match the booking room."
                )

        return cleaned_data
