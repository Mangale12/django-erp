from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from hotel_app.restaurant_menu.models import KDSLog


class KDSLogDataTable(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()

        base_queryset = KDSLog.objects.select_related(
            "kot_line",
            "kitchen",
            "station",
            "action_by",
        ).all()

        total_records = base_queryset.count()

        if search_value:
            base_queryset = base_queryset.filter(
                Q(action_taken__icontains=search_value)
                | Q(device_id__icontains=search_value)
                | Q(ip_address__icontains=search_value)
                | Q(kot_line__item_name_snapshot__icontains=search_value)
                | Q(kitchen__name__icontains=search_value)
                | Q(station__name__icontains=search_value)
                | Q(action_by__username__icontains=search_value)
            )

        filtered_records = base_queryset.count()
        paginated_queryset = base_queryset[start : start + length]

        data = [
            {
                "id": item.pk,
                "business_date": item.business_date.isoformat() if item.business_date else "-",
                "kot_line": item.kot_line.item_name_snapshot or f"Line {item.kot_line_id}",
                "kitchen": item.kitchen.name if item.kitchen else "-",
                "station": item.station.name if item.station else "-",
                "action_taken": item.get_action_taken_display(),
                "action_by": item.action_by.username if item.action_by else "-",
                "action_timestamp": item.action_timestamp.isoformat() if item.action_timestamp else "-",
                "delay_reason": item.delay_reason or "-",
                "device_id": item.device_id or "-",
                "ip_address": item.ip_address or "-",
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
