from django import forms
from ..models.kitchen import Kitchen


class KitchenForm(forms.ModelForm):

    class Meta:
        model = Kitchen
        fields = [
            "code",
            "name",
            "type",
            "outlet",
            "printer_ip_address",
            "backup_printer_ip",
            "kds_display_id",
            "is_kds_enabled",
            "is_printer_enabled",
            "display_order",
            "is_active",
        ]

        widgets = {
            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Kitchen Code"
            }),
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Kitchen Name"
            }),
            "type": forms.Select(attrs={
                "class": "form-select"
            }),
            "outlet": forms.Select(attrs={
                "class": "form-select"
            }),
            "printer_ip_address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "192.168.1.10"
            }),
            "backup_printer_ip": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "192.168.1.11"
            }),
            "kds_display_id": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Display ID"
            }),
            "display_order": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "1"
            }),
            "is_kds_enabled": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "is_printer_enabled": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
