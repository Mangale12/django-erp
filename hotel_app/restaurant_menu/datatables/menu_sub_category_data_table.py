from core.datatables.base import BaseDataTable
from core.datatables.buttons import ActionButton
from core.datatables.actions import ActionGroup
from hotel_app.restaurant_menu.models import MenuSubCategory
from django.urls import reverse

class MenuSubCategoryDataTable(BaseDataTable):
    model = MenuSubCategory
    columns = [
        "id", "menu_category", "name", "code", "description", "is_active"
    ]
    search_fields = ["menu_category", "name", "code", "description", "is_active"]

    actions = ActionGroup(
        ActionButton(
            label="View",
            icon="eye",
            css="btn btn-outline-info btn-sm",
            url=lambda o: reverse("menu_sub_category_edit", args=[o.id]),
        ),
        ActionButton(
            label="Edit",
            icon="edit",
            css="btn btn-primary btn-sm",
            url=lambda o: "#",
            attrs={
                "id": lambda o: o.id,
                "url": lambda o: reverse("menu_sub_category_edit", args=[o.id]),
                "bs-toggle": "modal",
                "bs-target": "#menuSubCategoryModal",
            },
        ),
        ActionButton(
            label="Delete",
            icon="trash",
            css="btn btn-outline-danger btn-sm",
            url=lambda o: reverse("menu_sub_category_delete", args=[o.id]),
        ),
    )

    def get_queryset(self):
        return self.model.objects.select_related('menu_category').all()

    def get_row_data(self, obj):
        row = super().get_row_data(obj)

        row["menu_category"] = f"{obj.menu_category}"
        row["name"] = f"{obj.name}"
        row["code"] = f"{obj.code}"
        row["description"] = f"{obj.description}"
        row["is_active"] = f"{obj.is_active}"
        return row
