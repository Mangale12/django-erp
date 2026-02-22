from django.db import models


class FolioTransaction(models.Model):
    folio_trn_id = models.BigAutoField(primary_key=True)
    folio = models.ForeignKey("restaurant_menu.Folio", on_delete=models.CASCADE, related_name="transactions")
    source_module_id = models.CharField(max_length=100)
    reference_id = models.BigIntegerField()
    debit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    credit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    transaction_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Folio Transaction"
        verbose_name_plural = "Folio Transactions"
        ordering = ["-transaction_date", "-created_at"]

    def __str__(self):
        return f"FolioTrn #{self.folio_trn_id} - Folio #{self.folio_id}"
