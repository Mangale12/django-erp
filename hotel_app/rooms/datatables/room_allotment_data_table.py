from core.datatables.base import BaseDataTable
from core.datatables.buttons import ActionButton
from core.datatables.actions import ActionGroup
from hotel_app.rooms.models import RoomAllotment
from django.urls import reverse

class RoomAllotmentDataTable(BaseDataTable):
    model = RoomAllotment
    columns = [
        "id", "booking", "room", "alloted_by", "alloted_at"
    ]
    search_fields = ["booking", "room", "alloted_by", "alloted_at"]

    actions = ActionGroup(
        ActionButton(
            label="View",
            icon="eye",
            css="btn btn-outline-info btn-sm",
            url=lambda o: reverse("room_allotment_view", args=[o.id]),
        ),
        ActionButton(
            label="Edit",
            icon="edit",
            css="btn btn-primary btn-sm",
            url=lambda o: "#",
            attrs={
                "id": lambda o: o.id,
                "url": lambda o: reverse("room_allotment_edit", args=[o.id]),
                "bs-toggle": "modal",
                "bs-target": "#roomAllotmentModal",
            },
        ),
        ActionButton(
            label="Delete",
            icon="trash",
            css="btn btn-outline-danger btn-sm",
            url=lambda o: reverse("room_allotment_delete", args=[o.id]),
        ),
    )

    def get_queryset(self):
        """
        Example of complex query:
        Join with other tables, annotate, prefetch related
        """
        return self.model.objects.select_related('room', 'booking', 'alloted_by').all()

    def get_row_data(self, obj):
        """
        Only override for custom fields or computed logic
        Everything else (FK, date, boolean) is handled by BaseDataTable
        """
        row = super().get_row_data(obj)

        # Example: Add computed field
        return row
