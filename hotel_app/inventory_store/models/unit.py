import django.db.models as models


class Unit(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the unit (max 256 characters)')
    symbol = models.CharField(max_length=10, unique=True, null=True, blank=True, help_text='Symbol of the unit (max 10 characters)')
    conversion_factor = models.DecimalField(max_digits=10, decimal_places=2, default=1, help_text='Conversion factor of the unit')
    is_active = models.BooleanField(default=True, help_text='Is the unit active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the unit was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the unit was last updated')

    def __str__(self):
        return self.name