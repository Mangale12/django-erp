from django.db import models

class KOTStatus(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True, help_text="Name of the KOT status")
    code = models.CharField(max_length=250, null=True, blank=True, help_text="Code of the KOT status")
    description = models.TextField(null=True, blank=True, help_text="Description of the KOT status")
    is_active = models.BooleanField(default=True, help_text="Is the KOT status active?")
    create_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_statuses_create_by', null=True, blank=True, help_text="User who created the KOT status")
    create_at = models.DateTimeField(auto_now_add=True, help_text="Create at for the KOT status")
    update_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_statuses_update_by', null=True, blank=True, help_text="User who updated the KOT status")
    update_at = models.DateTimeField(auto_now=True, help_text="Update at for the KOT status")

    def __str__(self):
        return self.name