from django import forms
from .models import KOTStatus

class KotStatusForm(forms.ModelForm):
    class Meta:
        model = KOTStatus
        fields = '__all__'