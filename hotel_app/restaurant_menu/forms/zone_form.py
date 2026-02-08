from django import forms
from hotel_app.restaurant_menu.models import Zone


class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'
    