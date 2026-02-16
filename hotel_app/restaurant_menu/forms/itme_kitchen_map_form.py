from django import forms
from ..models import ItemKitchenMap

class ItemKitchenMapForm(forms.ModelForm):
    class Meta:
        model = ItemKitchenMap
        fields = '__all__'
        widgets = {
            'menu_item': forms.Select(attrs={'class': 'form-control'}),
            'kitchen': forms.Select(attrs={'class': 'form-control'}),
            'kitchen_station': forms.Select(attrs={'class': 'form-control'}),
            'expected_time': forms.NumberInput(attrs={'class': 'form-control'}),
        }