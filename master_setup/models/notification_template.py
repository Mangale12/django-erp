import django.db.models as models

class NotificationTemplate(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the notification template (max 256 characters)')
    code = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Code of the notification template (max 256 characters)')
    channel = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Channel of the notification template (max 256 characters)')
    notification_category = models.ForeignKey('NotificationCategory', on_delete=models.CASCADE, null=True, blank=True, help_text='Notification category of the notification template')
    message_body = models.TextField(null=True, blank=True, help_text='Message body of the notification template')
    is_active = models.BooleanField(default=True, help_text='Is the notification template active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the notification template was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the notification template was last updated')

    def __str__(self):
        return self.name
