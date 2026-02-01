import django.db.models as models


class ShiftType(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the shift type (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the shift type (max 256 characters)')
    start_time = models.TimeField(null=True, blank=True, help_text='Start time of the shift type')
    end_time = models.TimeField(null=True, blank=True, help_text='End time of the shift type')
    break_duration = models.DurationField(null=True, blank=True, help_text='Break duration of the shift type')
    is_active = models.BooleanField(default=True, help_text='Is the shift type active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the shift type was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the shift type was last updated')

    def __str__(self):
        return self.name