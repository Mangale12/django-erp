from django import forms
from ..models import KitchenStation

class KitchenStationForm(forms.ModelForm):
    class Meta:
        model = KitchenStation
        fields = ['name', 'kitchen', 'printer', 'kds_display_id', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'kitchen': forms.Select(attrs={'class': 'form-control'}),
            'printer': forms.Select(attrs={'class': 'form-control'}),
            'kds_display_id': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }