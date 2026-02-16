from django.db import models

class KOTType(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True, help_text="Name of the KOT type")
    code = models.CharField(max_length=250, null=True, blank=True, help_text="Code of the KOT type")
    description = models.TextField(null=True, blank=True, help_text="Description of the KOT type")
    is_active = models.BooleanField(default=True, help_text="Is the KOT type active?")
    create_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_types_create_by', null=True, blank=True, help_text="User who created the KOT type")
    create_at = models.DateTimeField(auto_now_add=True, help_text="Create at for the KOT type")
    update_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='kot_types_update_by', null=True, blank=True, help_text="User who updated the KOT type")
    update_at = models.DateTimeField(auto_now=True, help_text="Update at for the KOT type")

    def __str__(self):
        return self.name
