from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from hotel_app.restaurant_menu.models import Kitchen


class KitchenDataTable(View):

    def get(self, request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()

        base_queryset = Kitchen.objects.all()

        # Total records before filtering
        total_records = base_queryset.count()

        # Search filter
        if search_value:
            base_queryset = base_queryset.filter(
                Q(kitchen_code__icontains=search_value) |
                Q(kitchen_name__icontains=search_value) |
                Q(kitchen_type__icontains=search_value) |
                Q(outlet__outlet_name__icontains=search_value)
            )

        # Records after filtering
        filtered_records = base_queryset.count()

        # Pagination
        paginated_queryset = base_queryset.order_by('-created_at')[start:start + length]

        data = [
            {
                "id": item.id,
                "kitchen_code": item.kitchen_code,
                "kitchen_name": item.kitchen_name,
                "kitchen_type": item.get_kitchen_type_display(),
                "outlet": item.outlet.outlet_name,
            }
            for item in paginated_queryset
        ]

        return JsonResponse({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": data
        })
