from django.conf import settings
from django.db import models


class KOTCourseControl(models.Model):
    FIRE_STATUS_CHOICES = (
        ("HOLD", "Hold"),
        ("FIRED", "Fired"),
        ("COMPLETED", "Completed"),
    )

    course_control_id = models.BigAutoField(primary_key=True, db_column="Course_Control_ID")
    kot = models.ForeignKey(
        "KOTHeader",
        on_delete=models.CASCADE,
        related_name="course_controls",
        db_column="KOT_ID",
    )
    course_number = models.PositiveIntegerField(db_column="Course_Number")
    fire_status = models.CharField(max_length=20, choices=FIRE_STATUS_CHOICES, default="HOLD", db_column="Fire_Status")
    hold_until_time = models.TimeField(blank=True, null=True, db_column="Hold_Until_Time")
    fired_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="fired_kot_courses",
        blank=True,
        null=True,
        db_column="Fired_By",
    )
    fired_timestamp = models.DateTimeField(blank=True, null=True, db_column="Fired_Timestamp")

    class Meta:
        db_table = "trn_kot_course_control"
        verbose_name = "KOT Course Control"
        verbose_name_plural = "KOT Course Controls"
        ordering = ["-course_control_id"]

    def __str__(self):
        return f"{self.kot_id} | Course {self.course_number} | {self.get_fire_status_display()}"
