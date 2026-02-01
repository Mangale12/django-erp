import django.db.models as models

class ParkingType(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the parking type (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the parking type (max 256 characters)')
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Rate of the parking type')
    description = models.TextField(null=True, blank=True, help_text='Description of the parking type')
    is_active = models.BooleanField(default=True, help_text='Is the parking type active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the parking type was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the parking type was last updated')

    def __str__(self):
        return self.name