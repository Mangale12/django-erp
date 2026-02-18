from django.conf import settings
from django.db import models
from django.utils import timezone


class KDSLog(models.Model):
    ACTION_CHOICES = (
        ("FIRE", "Fire"),
        ("START", "Start"),
        ("BUMP", "Bump"),
        ("RECALL", "Recall"),
        ("DELAY", "Delay"),
        ("CANCEL", "Cancel"),
    )

    business_date = models.DateField(db_column="Business_Date")
    kot_line = models.ForeignKey("KOTLineItem", on_delete=models.CASCADE, related_name="kds_logs", blank=True, null=True, help_text="KOT line for the KDS log")
    kitchen = models.ForeignKey("Kitchen", on_delete=models.CASCADE, related_name="kds_logs", blank=True, null=True, help_text="Kitchen for the KDS log")
    station = models.ForeignKey("KitchenStation", on_delete=models.CASCADE, related_name="kds_logs", blank=True, null=True, help_text="Kitchen station for the KDS log")
    action_taken = models.CharField(max_length=20, choices=ACTION_CHOICES, db_column="Action_Taken")
    action_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="kds_logs_actions", blank=True, null=True, help_text="User who took the action")
    action_timestamp = models.DateTimeField(default=timezone.now)
    delay_reason = models.TextField(blank=True, null=True, help_text="Reason for delay")
    device_id = models.CharField(max_length=100, blank=True, null=True, help_text="Device ID")
    ip_address = models.GenericIPAddressField(blank=True, null=True, help_text="IP address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "KDS Log"
        verbose_name_plural = "KDS Logs"
        ordering = ["-action_timestamp", "-created_at"]

    def __str__(self):
        return {self.get_action_taken_display()}
