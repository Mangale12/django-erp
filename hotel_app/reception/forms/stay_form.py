from django import forms
from django.core.exceptions import ValidationError

from hotel_app.reception.models import Stay


class StayForm(forms.ModelForm):
    class Meta:
        model = Stay
        fields = [
            "guest",
            "booking",
            "check_in",
            "check_out",
            "room",
            "check_in_date",
            "expected_check_out_date",
            "actual_check_out_date",
            "stay_status",
            "remarks",
        ]

    def clean(self):
        cleaned_data = super().clean()

        guest = cleaned_data.get("guest")
        booking = cleaned_data.get("booking")
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        room = cleaned_data.get("room")
        check_in_date = cleaned_data.get("check_in_date")
        expected_check_out_date = cleaned_data.get("expected_check_out_date")
        actual_check_out_date = cleaned_data.get("actual_check_out_date")

        if booking and guest and booking.guest_id != guest.id:
            raise ValidationError("Selected booking does not belong to the selected guest.")

        if check_in and guest and check_in.guest_id != guest.id:
            raise ValidationError("Selected check-in does not belong to the selected guest.")

        if check_out and guest and check_out.guest_id != guest.id:
            raise ValidationError("Selected check-out does not belong to the selected guest.")

        if booking and room and booking.room_id != room.id:
            raise ValidationError("Selected room does not match the booking room.")

        if check_in and room and check_in.room_id != room.id:
            raise ValidationError("Selected room does not match the check-in room.")

        if check_in_date and expected_check_out_date and expected_check_out_date < check_in_date:
            raise ValidationError("Expected check-out date must be after check-in date.")

        if check_in_date and actual_check_out_date and actual_check_out_date < check_in_date:
            raise ValidationError("Actual check-out date must be after check-in date.")

        return cleaned_data
