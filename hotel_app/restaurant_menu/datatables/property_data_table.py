from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from hotel_app.restaurant_menu.models import Property


class PropertyDataTable(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()

        base_queryset = Property.objects.select_related("parent_property").all()
        total_records = base_queryset.count()

        if search_value:
            base_queryset = base_queryset.filter(
                Q(property_code__icontains=search_value)
                | Q(property_name__icontains=search_value)
                | Q(property_type__icontains=search_value)
                | Q(city__icontains=search_value)
                | Q(state__icontains=search_value)
                | Q(country__icontains=search_value)
                | Q(phone__icontains=search_value)
                | Q(email__icontains=search_value)
            )

        filtered_records = base_queryset.count()
        paginated_queryset = base_queryset.order_by("-created_at")[start : start + length]

        data = [
            {
                "id": item.id,
                "property_code": item.property_code,
                "property_name": item.property_name,
                "property_type": item.get_property_type_display(),
                "city": item.city,
                "state": item.state,
                "country": item.country,
                "phone": item.phone,
                "email": item.email,
                "parent_property": item.parent_property.property_name if item.parent_property else "-",
                "is_active": item.is_active,
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
