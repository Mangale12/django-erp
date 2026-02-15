from django import forms
from .models import KitchenType

class KitchenTypeForm(forms.ModelForm):
    class Meta:
        model = KitchenType
        fields = '__all__'
        