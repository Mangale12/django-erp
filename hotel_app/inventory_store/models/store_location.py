import django.db.models as models


class StoreLocation(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the store location (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the store location (max 256 characters)')
    location = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Location of the store location (max 256 characters)')
    description = models.TextField(null=True, blank=True, help_text='Description of the store location')
    is_active = models.BooleanField(default=True, help_text='Is the store location active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the store location was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the store location was last updated')

    def __str__(self):
        return self.name
