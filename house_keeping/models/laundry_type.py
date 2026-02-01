import django.db.models as models

class LaundryType(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the laundry type (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the laundry type (max 256 characters)')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Price of the laundry type')
    description = models.TextField(null=True, blank=True, help_text='Description of the laundry type')
    is_active = models.BooleanField(default=True, help_text='Is the laundry type active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the laundry type was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the laundry type was last updated')

    def __str__(self):
        return self.name