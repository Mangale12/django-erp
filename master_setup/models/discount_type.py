import django.db.models as models

class DiscountType(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the discount type (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the discount type (max 256 characters)')
    discount_type = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Type of the discount type (max 256 characters)')
    description = models.TextField(null=True, blank=True, help_text='Description of the discount type')
    is_active = models.BooleanField(default=True, help_text='Is the discount type active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the discount type was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the discount type was last updated')

    def __str__(self):
        return self.name
