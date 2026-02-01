from core.datatables.base import BaseDataTable
from core.datatables.buttons import ActionButton
from core.datatables.actions import ActionGroup
from hotel_app.restaurant.models import MenuCategory
from django.urls import reverse

class MenuCategoryDataTable(BaseDataTable):
    model = MenuCategory
    columns = [
        "id", "name", "code", "description", "is_active"
    ]
    search_fields = ["name", "code", "description", "is_active"]

    actions = ActionGroup(
        ActionButton(
            label="View",
            icon="eye",
            css="btn btn-outline-info btn-sm",
            url=lambda o: reverse("menu_category_edit", args=[o.id]),
        ),
        ActionButton(
            label="Edit",
            icon="edit",
            css="btn btn-primary btn-sm",
            url=lambda o: "#",
            attrs={
                "id": lambda o: o.id,
                "url": lambda o: reverse("menu_category_edit", args=[o.id]),
                "bs-toggle": "modal",
                "bs-target": "#menuCategoryModal",
            },
        ),
        ActionButton(
            label="Delete",
            icon="trash",
            css="btn btn-outline-danger btn-sm",
            url=lambda o: reverse("menu_category_delete", args=[o.id]),
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
        return row
