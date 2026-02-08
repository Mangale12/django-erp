from django import forms
from hotel_app.restaurant_menu.models import TableSetup, Zone

class TableSetupForm(forms.ModelForm):
    class Meta:
        model = TableSetup
        fields = ['name', 'seating_capacity', 'location_area', 'is_active', 'zone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['zone'].queryset = Zone.objects.all()
        self.fields['zone'].label_from_instance = lambda obj: obj.name