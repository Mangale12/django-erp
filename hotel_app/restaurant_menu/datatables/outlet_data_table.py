from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from hotel_app.restaurant_menu.models import Outlet


class OutletDataTable(View):

    def get(self, request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()

        base_queryset = Outlet.objects.all()

        # Total records before filtering
        total_records = base_queryset.count()

        # Search filter
        if search_value:
            base_queryset = base_queryset.filter(
                Q(outlet_code__icontains=search_value) |
                Q(outlet_name__icontains=search_value) |
                Q(outlet_type__icontains=search_value) |
                Q(location_description__icontains=search_value)
            )

        # Records after filtering
        filtered_records = base_queryset.count()

        # Pagination
        paginated_queryset = base_queryset.order_by('-created_at')[start:start + length]

        data = [
            {
                "id": item.id,
                "outlet_code": item.outlet_code,
                "outlet_name": item.outlet_name,
                "outlet_type": item.get_outlet_type_display(),
                "location_description": item.location_description,
                "service_charge_percentage": float(item.service_charge_percentage),
                "vat_percentage": float(item.vat_percentage),
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
