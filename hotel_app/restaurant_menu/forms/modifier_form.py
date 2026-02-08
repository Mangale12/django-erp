from django import forms
from hotel_app.restaurant_menu.models import Modifier
from hotel_app.restaurant_menu.models import MenuItem

class ModifierForm(forms.ModelForm):
    class Meta:
        model = Modifier
        fields = ['name', 'extra_price', 'description', 'is_active', 'menu_item']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_item'].queryset = MenuItem.objects.all()
        self.fields['menu_item'].label_from_instance = lambda obj: obj.name