from django.conf import settings
from django.db import models
from django.utils import timezone


class KOTReprintLog(models.Model):
    reprint_log_id = models.BigAutoField(primary_key=True, db_column="Reprint_Log_ID")
    kot = models.ForeignKey(
        "KOTHeader",
        on_delete=models.CASCADE,
        related_name="reprint_logs",
        db_column="KOT_ID",
    )
    reprinted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reprinted_kots",
        db_column="Reprinted_By",
    )
    reprint_timestamp = models.DateTimeField(default=timezone.now, db_column="Reprint_Timestamp")
    reason = models.TextField(db_column="Reason")

    class Meta:
        db_table = "trn_kot_reprint_logs"
        verbose_name = "KOT Reprint Log"
        verbose_name_plural = "KOT Reprint Logs"
        ordering = ["-reprint_timestamp", "-reprint_log_id"]

    def __str__(self):
        return f"{self.reprint_log_id} | {self.kot_id}"
