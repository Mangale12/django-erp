from django import forms
from .models import Outlet


class OutletForm(forms.ModelForm):
    
    class Meta:
        model = Outlet
        fields = '__all__'
        
        widgets = {
            "opening_time": forms.TimeInput(attrs={"type": "time"}),
            "closing_time": forms.TimeInput(attrs={"type": "time"}),
            "business_day_start_time": forms.TimeInput(attrs={"type": "time"}),
            
            "service_charge_percentage": forms.NumberInput(attrs={"step": "0.01"}),
            "vat_percentage": forms.NumberInput(attrs={"step": "0.01"}),
        }
