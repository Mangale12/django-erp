import django.db.models as models


class MenuItem(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the menu item (max 256 characters)')
    code = models.CharField(max_length=250, unique=True, null=True, blank=True, help_text='A short code to identify the menu item (max 50 characters)')
    menu_category = models.ForeignKey('MenuCategory', on_delete=models.CASCADE, help_text='Menu category to which the menu item belongs')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price of the menu item')
    description = models.TextField(blank=True, help_text='Description of the menu item')
    is_active = models.BooleanField(default=True, help_text='Is the menu item active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the menu item was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the menu item was last updated')

    def __str__(self):
        return self.name
    