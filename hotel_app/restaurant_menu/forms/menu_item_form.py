from django import forms
from hotel_app.restaurant_menu.models import MenuItem, MenuCategory, MenuSubCategory
from master_setup.models import TaxType, FoodType, Printer


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            'name',
            'code',
            'menu_category',
            'menu_sub_category',
            'price',
            'description',
            'tax_type',
            'food_type',
            'recipe_linked',
            'printer',
            'is_active'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_category'].queryset = MenuCategory.objects.all()
        self.fields['menu_sub_category'].queryset = MenuSubCategory.objects.all()
        self.fields['tax_type'].queryset = TaxType.objects.all()
        self.fields['food_type'].queryset = FoodType.objects.all()
        self.fields['printer'].queryset = Printer.objects.all()
        