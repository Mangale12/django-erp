from django import forms
from ..models import KDSLog


class KDSLogForm(forms.ModelForm):
    class Meta:
        model = KDSLog
        fields = "__all__"