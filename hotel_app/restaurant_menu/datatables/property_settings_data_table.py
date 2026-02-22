from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from hotel_app.restaurant_menu.models import PropertySettings


class PropertySettingsDataTable(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()

        base_queryset = PropertySettings.objects.select_related("property").all()
        total_records = base_queryset.count()

        if search_value:
            base_queryset = base_queryset.filter(
                Q(property__property_code__icontains=search_value)
                | Q(property__property_name__icontains=search_value)
            )

        filtered_records = base_queryset.count()
        paginated_queryset = base_queryset.order_by("-created_at")[start : start + length]

        data = [
            {
                "id": item.pk,
                "property_code": item.property.property_code,
                "property_name": item.property.property_name,
                "enable_kot_module": item.enable_kot_module,
                "enable_table_management": item.enable_table_management,
                "enable_room_module": item.enable_room_module,
                "enable_folio_module": item.enable_folio_module,
                "enable_laundry_module": item.enable_laundry_module,
                "enable_spa_module": item.enable_spa_module,
                "enable_inventory_module": item.enable_inventory_module,
                "enable_credit_sales": item.enable_credit_sales,
                "enable_multi_outlet": item.enable_multi_outlet,
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
