import django.db.models as models

class MiscellaneousService(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the miscellaneous services (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the miscellaneous services (max 256 characters)')
    description = models.TextField(null=True, blank=True, help_text='Description of the miscellaneous services')
    chargeable = models.BooleanField(default=True, help_text='Is the miscellaneous services chargeable?')
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Rate of the miscellaneous services')
    is_active = models.BooleanField(default=True, help_text='Is the miscellaneous services active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the miscellaneous services was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the miscellaneous services was last updated')

    def __str__(self):
        return self.name