import django.db.models as models


class EmployeeType(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the employee type (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the employee type (max 256 characters)')
    description = models.TextField(null=True, blank=True, help_text='Description of the employee type')
    is_active = models.BooleanField(default=True, help_text='Is the employee type active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the employee type was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the employee type was last updated')

    def __str__(self):
        return self.name
