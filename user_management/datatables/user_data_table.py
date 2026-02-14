from core.datatables.base import BaseDataTable
from core.datatables.buttons import ActionButton
from core.datatables.actions import ActionGroup
from django.contrib.auth.models import User

from django.urls import reverse

class UserDataTable(BaseDataTable):
    model = User
    columns = [
        "id", "username", "email", "first_name", "last_name", "is_active", "is_staff", "is_superuser", "last_login", "date_joined"
    ]
    search_fields = ["username", "email", "first_name", "last_name", "is_active", "is_staff", "is_superuser", "last_login", "date_joined"]

    actions = ActionGroup(
        ActionButton(
            label="View",
            icon="eye",
            css="btn btn-outline-info btn-sm",
            url=lambda o: reverse("user_edit", args=[o.id]),
        ),
        ActionButton(
            label="Edit",
            icon="edit",
            css="btn btn-primary btn-sm",
            url=lambda o: "#",
            attrs={
                "id": lambda o: o.id,
                "url": lambda o: reverse("user_edit", args=[o.id]),
                "bs-toggle": "modal",
                "bs-target": "#userModal",
            },
        ),
        ActionButton(
            label="Delete",
            icon="trash",
            css="btn btn-outline-danger btn-sm",
            url=lambda o: reverse("user_delete", args=[o.id]),
        ),
    )

    def get_queryset(self):
        """
        Example of complex query:
        Join with other tables, annotate, prefetch related
        """
        return self.model.objects.all()

    def get_row_data(self, obj):
        """
        Only override for custom fields or computed logic
        Everything else (FK, date, boolean) is handled by BaseDataTable
        """
        row = super().get_row_data(obj)

        # Example: Add computed field
        row["full_name"] = f"{obj.first_name} {obj.last_name}"
        return row
