from core.datatables.base import BaseDataTable
from core.datatables.buttons import ActionButton
from core.datatables.actions import ActionGroup
from hotel_app.rooms.models import Room
from django.urls import reverse

class RoomDataTable(BaseDataTable):
    model = Room
    columns = [
        "id", "room_number", "room_type", "room_category", "floor", "view_type", "amenities", "current_status", "remarks", "is_active", "created_at", "updated_at"
    ]
    search_fields = ["room_number", "room_type", "room_category", "floor", "view_type", "amenities", "current_status", "remarks", "is_active", "created_at", "updated_at"]

    actions = ActionGroup(
        ActionButton(
            label="View",
            icon="eye",
            css="btn btn-outline-info btn-sm",
            url=lambda o: reverse("room_edit", args=[o.id]),
        ),
        ActionButton(
            label="Edit",
            icon="edit",
            css="btn btn-primary btn-sm",
            url=lambda o: "#",
            attrs={
                "id": lambda o: o.id,
                "url": lambda o: reverse("room_edit", args=[o.id]),
                "bs-toggle": "modal",
                "bs-target": "#roomModal",
            },
        ),
        ActionButton(
            label="Delete",
            icon="trash",
            css="btn btn-outline-danger btn-sm",
            url=lambda o: reverse("room_delete", args=[o.id]),
        ),
    )

    def get_queryset(self):
        """
        Example of complex query:
        Join with other tables, annotate, prefetch related
        """
        return self.model.objects.select_related('room_type', 'room_category', 'floor', 'view_type').all()

    def get_row_data(self, obj):
        """
        Only override for custom fields or computed logic
        Everything else (FK, date, boolean) is handled by BaseDataTable
        """
        row = super().get_row_data(obj)

        # Example: Add computed field
        row["amenities"] = ", ".join([str(a) for a in obj.amenities.all()])
        return row
