from django import forms
from django.core.exceptions import ValidationError
from hotel_app.rooms.models import RoomRate

class RoomRateForm(forms.ModelForm):

    class Meta:
        model = RoomRate
        fields = [
            'name',
            'code',
            'rate',
            'capacity',
            'extra_bed_charge',
            'tax_type',
            'is_active',
        ]

    def clean_rate(self):
        rate = self.cleaned_data.get('rate')
        if rate is not None and rate < 0:
            raise ValidationError("Rate cannot be negative.")
        return rate

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity is not None and capacity < 0:
            raise ValidationError("Capacity cannot be negative.")
        return capacity

    def clean_extra_bed_charge(self):
        extra_bed_charge = self.cleaned_data.get('extra_bed_charge')
        if extra_bed_charge is not None and extra_bed_charge < 0:
            raise ValidationError("Extra bed charge cannot be negative.")
        return extra_bed_charge

    
