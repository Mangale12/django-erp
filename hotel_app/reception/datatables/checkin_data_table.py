from core.datatables.base import BaseDataTable
from core.datatables.buttons import ActionButton
from core.datatables.actions import ActionGroup
from hotel_app.reception.models import CheckIn
from django.urls import reverse

class CheckInDataTable(BaseDataTable):
    model = CheckIn
    columns = [
        "id", "guest", "booking", "room", "user", "payment_mode", "advance_amount", "check_in_time", "remarks"
    ]
    search_fields = ["guest", "booking", "room", "user", "payment_mode", "advance_amount", "check_in_time", "remarks"]

    actions = ActionGroup(
        ActionButton(
            label="View",
            icon="eye",
            css="btn btn-outline-info btn-sm",
            url=lambda o: reverse("checkin_edit", args=[o.id]),
        ),
        ActionButton(
            label="Edit",
            icon="edit",
            css="btn btn-primary btn-sm",
            url=lambda o: "#",
            attrs={
                "id": lambda o: o.id,
                "url": lambda o: reverse("checkin_edit", args=[o.id]),
                "bs-toggle": "modal",
                "bs-target": "#checkinModal",
            },
        ),
        ActionButton(
            label="Delete",
            icon="trash",
            css="btn btn-outline-danger btn-sm",
            url=lambda o: reverse("checkin_delete", args=[o.id]),
        ),
    )

    def get_queryset(self):
        """
        Example of complex query:
        Join with other tables, annotate, prefetch related
        """
        return self.model.objects.select_related('booking', 'room', 'user', 'payment_mode').all()

    def get_row_data(self, obj):
        """
        Only override for custom fields or computed logic
        Everything else (FK, date, boolean) is handled by BaseDataTable
        """
        row = super().get_row_data(obj)

        # Example: Add computed field
        row["booking"] = f"{obj.booking}"
        row["room"] = f"{obj.room}"
        row["user"] = f"{obj.user}"
        row["payment_mode"] = f"{obj.payment_mode}"
        row["advance_amount"] = f"{obj.advance_amount}"
        row["check_in_time"] = f"{obj.check_in_time}"
        row["remarks"] = f"{obj.remarks}"
        return row
