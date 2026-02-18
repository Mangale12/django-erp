from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from hotel_app.restaurant_menu.models import KOTHeader

class KOTHeaderDataTable(View):
    def get(self, request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()

        base_queryset = KOTHeader.objects.all()

        total_records = base_queryset.count()  # ✅ QUERY 1

        if search_value:
            base_queryset = base_queryset.filter(
                Q(kot_number__icontains=search_value) |
                Q(outlet__name__icontains=search_value) |
                Q(table__name__icontains=search_value) |
                Q(guest__name__icontains=search_value) |
                Q(kitchen__name__icontains=search_value) |
                Q(kot_type__name__icontains=search_value) |
                Q(kot_status__name__icontains=search_value) |
                Q(priority_level__name__icontains=search_value)
            )

        filtered_records = base_queryset.count()  # ✅ QUERY 2 (only if searched)

        paginated_queryset = base_queryset[start:start + length]  # ✅ QUERY 3

        data = [
            {
                "id": item.id,
                "kot_number": item.kot_number,
                "outlet": item.outlet.outlet_name,
                "table": item.table.name if item.table else "-",
                "guest": item.guest.name if item.guest else "-",
                "kitchen": item.kitchen.name if item.kitchen else "-",
                "cover_count": item.cover_count,
                "kot_type": item.kot_type.name if item.kot_type else "-",
                "kot_status": item.kot_status.name if item.kot_status else "-",
                "priority_level": item.priority_level.name if item.priority_level else "-",
                "is_urgent": item.is_urgent,
                "is_reprint": item.is_reprint,
                "reprint_count": item.reprint_count,
                "printed_at": item.printed_at.isoformat() if item.printed_at else "-",
                "completed_at": item.completed_at.isoformat() if item.completed_at else "-",
                "total_item_count": item.total_item_count,
                "total_quantity": item.total_quantity,
                "is_stock_posted": item.is_stock_posted,
                "stock_posted_at": item.stock_posted_at.isoformat() if item.stock_posted_at else "-",
                "order": item.order.order_number if item.order else "-",
                "shift": item.shift_type.name if item.shift_type else "-",
                "room": item.room.room_number if item.room else "-",
            }
            for item in paginated_queryset
        ]

        return JsonResponse({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": data
        })
