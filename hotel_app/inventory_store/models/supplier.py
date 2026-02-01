import django.db.models as models


class Supplier(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the supplier (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the supplier (max 256 characters)')
    contact_number = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Contact number of the supplier (max 256 characters)')
    email = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Email of the supplier (max 256 characters)')
    address = models.TextField(null=True, blank=True, help_text='Address of the supplier')
    is_active = models.BooleanField(default=True, help_text='Is the supplier active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the supplier was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the supplier was last updated')

    def __str__(self):
        return self.name