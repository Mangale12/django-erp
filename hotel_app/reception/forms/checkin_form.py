from django import forms
from django.core.exceptions import ValidationError
from hotel_app.reception.models import CheckIn

class CheckInForm(forms.ModelForm):

    class Meta:
        model = CheckIn
        fields = [
            'booking',
            'guest',
            'room',
            'payment_mode',
            'advance_amount',
            'remarks',
            'user',
        ]

    def clean_advance_amount(self):
        amount = self.cleaned_data.get('advance_amount')
        if amount is not None and amount < 0:
            raise ValidationError("Advance amount cannot be negative.")
        return amount

    def clean_booking(self):
        booking = self.cleaned_data.get('booking')

        # Prevent double check-in
        if CheckIn.objects.filter(booking=booking).exists():
            raise ValidationError("This booking is already checked in.")

        return booking

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
