from core.datatables.actions import ActionGroup
from core.datatables.base import BaseDataTable
from core.datatables.buttons import ActionButton
from django.urls import reverse

from hotel_app.reception.models import Stay


class StayDataTable(BaseDataTable):
    model = Stay
    columns = [
        "guest",
        "room",
        "check_in_date",
        "expected_check_out_date",
        "actual_check_out_date",
        "stay_status",
        "remarks",
    ]
    search_fields = [
        "guest__name",
        "room__room_number",
        "stay_status",
        "remarks",
    ]

    actions = ActionGroup(
        ActionButton(
            label="View",
            icon="eye",
            css="btn btn-outline-info btn-sm",
            url=lambda o: reverse("stay_edit", args=[o.id]),
        ),
        ActionButton(
            label="Edit",
            icon="edit",
            css="btn btn-primary btn-sm",
            url=lambda o: "#",
            attrs={
                "id": lambda o: o.id,
                "url": lambda o: reverse("stay_edit", args=[o.id]),
                "bs-toggle": "modal",
                "bs-target": "#stayModal",
            },
        ),
        ActionButton(
            label="Delete",
            icon="trash",
            css="btn btn-outline-danger btn-sm",
            url=lambda o: reverse("stay_delete", args=[o.id]),
        ),
    )

    def get_queryset(self):
        return self.model.objects.select_related("guest", "room").all()
