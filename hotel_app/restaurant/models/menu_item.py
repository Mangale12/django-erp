from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the menu item (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the menu item (max 256 characters)')
    menu_category = models.ForeignKey('MenuCategory', on_delete=models.CASCADE, related_name='menu_items', help_text='Menu category to which the menu item belongs')
    menu_sub_category = models.ForeignKey('MenuSubCategory', on_delete=models.CASCADE, related_name='menu_items', help_text='Menu sub category to which the menu item belongs')
    price = models.DecimalField(max_digits=10, decimal_places=2, unique=False, null=True, blank=True, help_text='Price of the menu item (max 10 digits, 2 decimal places)')
    description = models.TextField(unique=False, null=True, blank=True, help_text='Description of the menu item (max 256 characters)')
    tax_type = models.ForeignKey('master_setup.TaxType', on_delete=models.CASCADE, related_name='menu_items', null=True, blank=True, help_text='Tax type to which the menu item belongs')
    food_type = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Food type to which the menu item belongs')
    is_active = models.BooleanField(default=True, help_text='Is the menu item active?')
    recipe_linked = models.BooleanField(default=False, help_text='Is the menu item linked to a recipe?')
    printer_id = models.ForeignKey('master_setup.Printer', on_delete=models.CASCADE, related_name='menu_items', null=True, blank=True, help_text='Printer to which the menu item belongs')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the menu item was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the menu item was last updated')
    