from django.db import models

class PriorityLevel(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True, help_text="Name of the priority level")
    code = models.CharField(max_length=250, null=True, blank=True, help_text="Code of the priority level")
    description = models.TextField(null=True, blank=True, help_text="Description of the priority level")
    is_active = models.BooleanField(default=True, help_text="Is the priority level active?")
    create_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='priority_levels_create_by', null=True, blank=True, help_text="User who created the priority level")
    create_at = models.DateTimeField(auto_now_add=True, help_text="Create at for the priority level")
    update_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='priority_levels_update_by', null=True, blank=True, help_text="User who updated the priority level")
    update_at = models.DateTimeField(auto_now=True, help_text="Update at for the priority level")

    def __str__(self):
        return self.name
