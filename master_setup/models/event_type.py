import django.db.models as models

class EventType(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the event type (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the event type (max 256 characters)')
    default_capacity = models.IntegerField(null=True, blank=True, help_text='Default capacity of the event type')
    description = models.TextField(null=True, blank=True, help_text='Description of the event type')
    is_active = models.BooleanField(default=True, help_text='Is the event type active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the event type was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the event type was last updated')

    def __str__(self):
        return self.name