from django.db import models

class MenuSubCategory(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the menu sub category (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the menu sub category (max 256 characters)')
    description = models.TextField(unique=False, null=True, blank=True, help_text='Description of the menu sub category (max 256 characters)')
    is_active = models.BooleanField(default=True, help_text='Is the menu sub category active?')
    menu_category = models.ForeignKey('MenuCategory', on_delete=models.CASCADE, related_name='menu_sub_categories', help_text='Menu category to which the menu sub category belongs')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the menu sub category was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the menu sub category was last updated')

    def __str__(self):
        return self.name