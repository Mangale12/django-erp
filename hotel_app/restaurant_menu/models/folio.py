from django.db import models


class Folio(models.Model):
    FOLIO_STATUS_CHOICES = (
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
        ("SETTLED", "Settled"),
    )

    id = models.BigAutoField(primary_key=True)
    stay = models.ForeignKey("reception.Stay", on_delete=models.PROTECT, related_name="folios")
    total_debit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_credit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    folio_status = models.CharField(max_length=20, choices=FOLIO_STATUS_CHOICES, default="OPEN")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Folio"
        verbose_name_plural = "Folios"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.balance_amount = (self.total_debit or 0) - (self.total_credit or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Folio #{self.folio_id}"
