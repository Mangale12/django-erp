from django import forms
from django.core.exceptions import ValidationError
from hotel_app.restaurant_menu.models import MenuSubCategory

class MenuSubCategoryForm(forms.ModelForm):

    class Meta:
        model = MenuSubCategory
        fields = [
            'menu_category',
            'name',
            'code',
            'description',
            'is_active'
        ]

   

    
