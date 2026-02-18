from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from hotel_app.restaurant_menu.models import KOTAmendment


class KOTAmendmentDataTable(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()

        base_queryset = KOTAmendment.objects.select_related(
            "kot",
            "kot_line_item",
            "order",
            "original_item",
            "new_item",
            "manager",
            "amended_by",
        ).all()

        total_records = base_queryset.count()

        if search_value:
            base_queryset = base_queryset.filter(
                Q(action_type__icontains=search_value)
                | Q(reason_code__icontains=search_value)
                | Q(kot__kot_number__icontains=search_value)
                | Q(order__order_number__icontains=search_value)
                | Q(original_item__name__icontains=search_value)
                | Q(new_item__name__icontains=search_value)
                | Q(manager__username__icontains=search_value)
                | Q(amended_by__username__icontains=search_value)
            )

        filtered_records = base_queryset.count()
        paginated_queryset = base_queryset[start : start + length]

        data = [
            {
                "id": item.pk,
                "business_date": item.business_date.isoformat() if item.business_date else "-",
                "kot": item.kot.kot_number if item.kot else "-",
                "kot_line": item.kot_line_item.item_name_snapshot if item.kot_line_item else "-",
                "order": item.order.order_number if item.order else "-",
                "original_item": item.original_item.name if item.original_item else "-",
                "new_item": item.new_item.name if item.new_item else "-",
                "action_type": item.get_action_type_display(),
                "old_quantity": str(item.old_quantity),
                "new_quantity": str(item.new_quantity),
                "manager": item.manager.username if item.manager else "-",
                "reason_code": item.reason_code,
                "timestamp_amended": item.timestamp_amended.isoformat() if item.timestamp_amended else "-",
                "amended_by": item.amended_by.username if item.amended_by else "-",
            }
            for item in paginated_queryset
        ]

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": filtered_records,
                "data": data,
            }
        )
