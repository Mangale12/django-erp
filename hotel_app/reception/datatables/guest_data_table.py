from core.datatables.base import BaseDataTable
from core.datatables.buttons import ActionButton
from core.datatables.actions import ActionGroup
from hotel_app.reception.models import Guest
from django.urls import reverse

class GuestDataTable(BaseDataTable):
    model = Guest
    columns = [
        "id", "name", "phone", "email", "guest_type",
        "gender", "dob", "nationality", "id_proof_type", "id_proof_number",
        "address", "country", "state", "city", "is_active"
    ]
    search_fields = ["name", "phone", "email", "guest_type"]

    actions = ActionGroup(
        ActionButton(
            label="View",
            icon="eye",
            css="btn btn-outline-info btn-sm",
            url=lambda o: reverse("guest_edit", args=[o.id]),
        ),
        ActionButton(
            label="Edit",
            icon="edit",
            css="btn btn-primary btn-sm",
            url=lambda o: "#",
            attrs={
                "id": lambda o: o.id,
                "url": lambda o: reverse("guest_edit", args=[o.id]),
                "bs-toggle": "modal",
                "bs-target": "#guestModal",
            },
        ),
        ActionButton(
            label="Delete",
            icon="trash",
            css="btn btn-outline-danger btn-sm",
            url=lambda o: reverse("guest_delete", args=[o.id]),
        ),
    )

    def get_queryset(self):
        """
        Example of complex query:
        Join with other tables, annotate, prefetch related
        """
        return self.model.objects.select_related('country').all()

    def get_row_data(self, obj):
        """
        Only override for custom fields or computed logic
        Everything else (FK, date, boolean) is handled by BaseDataTable
        """
        row = super().get_row_data(obj)

        # Example: Add computed field
        row["full_address"] = f"{obj.address}, {obj.city}, {obj.state}"
        return row
