import django.db.models as models

class TaxType(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the tax type (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the tax type (max 256 characters)')
    tax_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text='Tax rate (e.g. 10.00 for 10%)')
    description = models.TextField(null=True, blank=True, help_text='Description of the tax type')
    is_active = models.BooleanField(default=True, help_text='Is the tax type active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the tax type was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the tax type was last updated')

    def __str__(self):
        return self.name
    