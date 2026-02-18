from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from hotel_app.restaurant_menu.models import KOTLineItem


class KOTLineItemDataTable(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()

        base_queryset = KOTLineItem.objects.select_related("kot", "item", "station").all()

        total_records = base_queryset.count()

        if search_value:
            base_queryset = base_queryset.filter(
                Q(kot__kot_number__icontains=search_value)
                | Q(item__name__icontains=search_value)
                | Q(item_code__icontains=search_value)
                | Q(item_status__icontains=search_value)
                | Q(priority_level__icontains=search_value)
            )

        filtered_records = base_queryset.count()

        paginated_queryset = base_queryset[start : start + length]

        data = [
            {
                "id": item.id,
                "kot": item.kot.kot_number if item.kot else "-",
                "item": item.item_name_snapshot or (item.item.name if item.item else "-"),
                "item_code": item.item_code or "-",
                "quantity": str(item.quantity),
                "uom": item.uom,
                "item_status": item.item_status,
                "priority_level": item.priority_level,
                "station": item.station.name if item.station else "-",
                "is_complimentary": item.is_complimentary,
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
