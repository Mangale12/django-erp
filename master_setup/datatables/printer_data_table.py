from core.datatables.base import BaseDataTable
from core.datatables.buttons import ActionButton
from core.datatables.actions import ActionGroup
from master_setup.models import Printer
from django.urls import reverse

class PrinterDataTable(BaseDataTable):
    model = Printer
    columns = [
        "id", "name", "code", "printer_type", "ip_address", "port", "is_active"
    ]
    search_fields = ["name", "code", "printer_type", "ip_address", "port", "is_active"]

    actions = ActionGroup(
        ActionButton(
            label="Edit",
            icon="edit",
            css="btn btn-primary btn-sm",
            url=lambda o: "#",
            attrs={
                "id": lambda o: o.id,
                "url": lambda o: reverse("printer_edit", args=[o.id]),
                "bs-toggle": "modal",
                "bs-target": "#printerModal",
            },
        ),
        ActionButton(
            label="Delete",
            icon="trash",
            css="btn btn-outline-danger btn-sm",
            url=lambda o: reverse("printer_delete", args=[o.id]),
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

        return row
