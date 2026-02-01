import django.db.models as models


class InventoryItem(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the inventory item (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the inventory item (max 256 characters)')
    item_type = models.ForeignKey('ItemType', on_delete=models.CASCADE, null=True, blank=True, help_text='Item type of the inventory item')
    item_category = models.ForeignKey('ItemCategory', on_delete=models.CASCADE, null=True, blank=True, help_text='Item category of the inventory item')
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, null=True, blank=True, help_text='Unit of the inventory item')
    minimum_stock = models.IntegerField(null=True, blank=True, help_text='Minimum stock of the inventory item')
    reorder_level = models.IntegerField(null=True, blank=True, help_text='Reorder level of the inventory item')
    is_active = models.BooleanField(default=True, help_text='Is the inventory item active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the inventory item was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the inventory item was last updated')

    def __str__(self):
        return self.name