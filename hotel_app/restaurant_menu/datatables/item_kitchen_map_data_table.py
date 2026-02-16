from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from hotel_app.restaurant_menu.models import ItemKitchenMap


class ItemKitchenMapDataTable(View):

    def get(self, request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()

        base_queryset = ItemKitchenMap.objects.all()

        # Total records before filtering
        total_records = base_queryset.count()

        # Search filter
        if search_value:
            base_queryset = base_queryset.filter(
                Q(menu_item__name__icontains=search_value) |
                Q(kitchen__name__icontains=search_value) |
                Q(kitchen_station__name__icontains=search_value) |
                Q(expected_time__icontains=search_value)
            )

        # Records after filtering
        filtered_records = base_queryset.count()

        # Pagination
        paginated_queryset = base_queryset.order_by('-created_at')[start:start + length]

        data = [
            {
                "id": item.id,
                "menu_item": item.menu_item.name,
                "kitchen": item.kitchen.name,
                "kitchen_station": item.kitchen_station.name,
                "expected_time": item.expected_time,
            }
            for item in paginated_queryset
        ]

        return JsonResponse({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": data
        })
