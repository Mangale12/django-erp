import django.db.models as models


class MenuCategory(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the menu category (max 256 characters)')
    code = models.CharField(max_length=250, unique=True, null=True, blank=True, help_text='A short code to identify the menu category (max 50 characters)')
    description = models.TextField(blank=True, help_text='Description of the menu category')
    is_active = models.BooleanField(default=True, help_text='Is the menu category active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the menu category was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the menu category was last updated')

    def __str__(self):
        return self.name