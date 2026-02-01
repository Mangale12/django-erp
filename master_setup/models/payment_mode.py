import django.db.models as models

class PaymentMode(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the payment mode (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the payment mode (max 256 characters)')
    description = models.TextField(null=True, blank=True, help_text='Description of the payment mode')
    is_active = models.BooleanField(default=True, help_text='Is the payment mode active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the payment mode was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the payment mode was last updated')

    def __str__(self):
        return self.name
    