from core.datatables.base import BaseDataTable
from core.datatables.buttons import ActionButton
from core.datatables.actions import ActionGroup
from hotel_app.reception.models import CheckOut
from django.urls import reverse

class CheckOutDataTable(BaseDataTable):
    model = CheckOut
    columns = [
        "id", "guest", "room", "user", "check_in", "check_out_time", "late_check_out_charge", "minibar_charge", "damage_charge", "other_charge", "final_bill_amount", "payment_mode", "remarks"
    ]
    search_fields = ["guest", "room", "user", "check_in", "check_out_time", "late_check_out_charge", "minibar_charge", "damage_charge", "other_charge", "final_bill_amount", "payment_mode", "remarks"]

    actions = ActionGroup(
        ActionButton(
            label="View",
            icon="eye",
            css="btn btn-outline-info btn-sm",
            url=lambda o: reverse("check_out_edit", args=[o.id]),
        ),
        ActionButton(
            label="Edit",
            icon="edit",
            css="btn btn-primary btn-sm",
            url=lambda o: "#",
            attrs={
                "id": lambda o: o.id,
                "url": lambda o: reverse("check_out_edit", args=[o.id]),
                "bs-toggle": "modal",
                "bs-target": "#checkoutModal",
            },
        ),
        ActionButton(
            label="Delete",
            icon="trash",
            css="btn btn-outline-danger btn-sm",
            url=lambda o: reverse("check_out_delete", args=[o.id]),
        ),
    )

    def get_queryset(self):
        """
        Example of complex query:
        Join with other tables, annotate, prefetch related
        """
        return self.model.objects.select_related('guest', 'room', 'user', 'check_in', 'payment_mode').all()

    def get_row_data(self, obj):
        """
        Only override for custom fields or computed logic
        Everything else (FK, date, boolean) is handled by BaseDataTable
        """
        row = super().get_row_data(obj)

        # Example: Add computed field
        row["guest"] = f"{obj.guest}"
        row["room"] = f"{obj.room}"
        row["user"] = f"{obj.user}"
        row["check_in"] = f"{obj.check_in}"
        row["check_out_time"] = f"{obj.check_out_time}"
        row["late_check_out_charge"] = f"{obj.late_check_out_charge}"
        row["minibar_charge"] = f"{obj.minibar_charge}"
        row["damage_charge"] = f"{obj.damage_charge}"
        row["other_charge"] = f"{obj.other_charge}"
        row["final_bill_amount"] = f"{obj.final_bill_amount}"
        row["payment_mode"] = f"{obj.payment_mode}"
        row["remarks"] = f"{obj.remarks}"
        return row
