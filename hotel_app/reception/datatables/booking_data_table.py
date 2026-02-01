from core.datatables.base import BaseDataTable
from core.datatables.buttons import ActionButton
from core.datatables.actions import ActionGroup
from hotel_app.reception.models import Booking
from django.urls import reverse

class BookingDataTable(BaseDataTable):
    model = Booking
    columns = [
        "id", "guest", "booking_source", "booking_date", "check_in_date", "check_out_date", "room", "no_of_adults", "no_of_children", "package_type", "discount_type", "discount_amount", "special_request", "booking_status", "remarks"
    ]
    search_fields = ["guest", "booking_source", "booking_date", "check_in_date", "check_out_date", "room", "no_of_adults", "no_of_children", "package_type", "discount_type", "discount_amount", "special_request", "booking_status", "remarks"]

    actions = ActionGroup(
        ActionButton(
            label="View",
            icon="eye",
            css="btn btn-outline-info btn-sm",
            url=lambda o: reverse("booking_edit", args=[o.id]),
        ),
        ActionButton(
            label="Edit",
            icon="edit",
            css="btn btn-primary btn-sm",
            url=lambda o: "#",
            attrs={
                "id": lambda o: o.id,
                "url": lambda o: reverse("booking_edit", args=[o.id]),
                "bs-toggle": "modal",
                "bs-target": "#bookingModal",
            },
        ),
        ActionButton(
            label="Delete",
            icon="trash",
            css="btn btn-outline-danger btn-sm",
            url=lambda o: reverse("booking_delete", args=[o.id]),
        ),
    )

    def get_queryset(self):
        """
        Example of complex query:
        Join with other tables, annotate, prefetch related
        """
        return self.model.objects.select_related('guest', 'booking_source', 'room').all()

    def get_row_data(self, obj):
        """
        Only override for custom fields or computed logic
        Everything else (FK, date, boolean) is handled by BaseDataTable
        """
        row = super().get_row_data(obj)

        # Example: Add computed field
        row["booking_date"] = f"{obj.booking_date.strftime('%Y-%m-%d')}"
        row["check_in_date"] = f"{obj.check_in_date.strftime('%Y-%m-%d')}"
        row["check_out_date"] = f"{obj.check_out_date.strftime('%Y-%m-%d')}"
        return row
