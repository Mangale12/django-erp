from django.db import models


class Stay(models.Model):
    STAY_STATUS_CHOICES = (
        ("CHECKED_IN", "Checked In"),
        ("CHECKED_OUT", "Checked Out"),
        ("CANCELLED", "Cancelled"),
    )

    id = models.BigAutoField(primary_key=True, serialize=False)
    guest = models.ForeignKey("Guest", on_delete=models.CASCADE, related_name="stays")
    booking = models.ForeignKey("Booking", on_delete=models.SET_NULL, null=True, blank=True, related_name="stays")
    check_in = models.ForeignKey("CheckIn", on_delete=models.SET_NULL, null=True, blank=True, related_name="stays")
    check_out = models.ForeignKey("CheckOut", on_delete=models.SET_NULL, null=True, blank=True, related_name="stays")
    room = models.ForeignKey("rooms.Room", on_delete=models.SET_NULL, null=True, blank=True, related_name="stays")
    check_in_date = models.DateTimeField()
    expected_check_out_date = models.DateTimeField(null=True, blank=True)
    actual_check_out_date = models.DateTimeField(null=True, blank=True)
    stay_status = models.CharField(max_length=20, choices=STAY_STATUS_CHOICES, default="CHECKED_IN")
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Stay"
        verbose_name_plural = "Stays"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Stay #{self.stay_id} - {self.guest}"
