from django import forms
from ..models import KOTType

class KotTypeForm(forms.ModelForm):
    class Meta:
        model = KOTType
        fields = '__all__'
