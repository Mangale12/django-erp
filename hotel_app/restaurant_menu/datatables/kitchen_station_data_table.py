from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from hotel_app.restaurant_menu.models import KitchenStation


class KitchenStationDataTable(View):

    def get(self, request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()

        base_queryset = KitchenStation.objects.all()

        # Total records before filtering
        total_records = base_queryset.count()

        # Search filter
        if search_value:
            base_queryset = base_queryset.filter(
                Q(name__icontains=search_value) |
                Q(kitchen__name__icontains=search_value) |
                Q(printer__name__icontains=search_value) |
                Q(kds_display_id__icontains=search_value)
            )

        # Records after filtering
        filtered_records = base_queryset.count()

        # Pagination
        paginated_queryset = base_queryset.order_by('-created_at')[start:start + length]

        data = [
            {
                "id": item.id,
                "name": item.name,
                "kitchen": item.kitchen.name,
                "printer": item.printer.name,
                "kds_display_id": item.kds_display_id,
                "is_active": item.is_active,
            }
            for item in paginated_queryset
        ]

        return JsonResponse({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": data
        })
