from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from hotel_app.restaurant_menu.models import KOTReprintLog


class KOTReprintLogDataTable(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()

        base_queryset = KOTReprintLog.objects.select_related("kot", "reprinted_by").all()
        total_records = base_queryset.count()

        if search_value:
            base_queryset = base_queryset.filter(
                Q(kot__kot_number__icontains=search_value)
                | Q(reprinted_by__username__icontains=search_value)
                | Q(reason__icontains=search_value)
            )

        filtered_records = base_queryset.count()
        paginated_queryset = base_queryset[start : start + length]

        data = [
            {
                "id": item.pk,
                "kot": item.kot.kot_number if item.kot else "-",
                "reprinted_by": item.reprinted_by.username if item.reprinted_by else "-",
                "reprint_timestamp": item.reprint_timestamp.isoformat() if item.reprint_timestamp else "-",
                "reason": item.reason,
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
