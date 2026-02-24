from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from hotel_app.restaurant_menu.models import SourceModule


class SourceModuleDataTable(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()

        base_queryset = SourceModule.objects.all()
        total_records = base_queryset.count()

        if search_value:
            base_queryset = base_queryset.filter(
                Q(module_name__icontains=search_value)
                | Q(module_code__icontains=search_value)
            )

        filtered_records = base_queryset.count()
        paginated_queryset = base_queryset.order_by("module_name")[start : start + length]

        data = [
            {
                "id": item.id,
                "module_name": item.module_name,
                "module_code": item.module_code,
                "is_postable_to_folio": item.is_postable_to_folio,
                "is_active": item.is_active,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
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
