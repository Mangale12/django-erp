from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from hotel_app.restaurant_menu.models import KOTCourseControl


class KOTCourseControlDataTable(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()

        base_queryset = KOTCourseControl.objects.select_related("kot", "fired_by").all()
        total_records = base_queryset.count()

        if search_value:
            base_queryset = base_queryset.filter(
                Q(kot__kot_number__icontains=search_value)
                | Q(course_number__icontains=search_value)
                | Q(fire_status__icontains=search_value)
                | Q(fired_by__username__icontains=search_value)
            )

        filtered_records = base_queryset.count()
        paginated_queryset = base_queryset[start : start + length]

        data = [
            {
                "id": item.pk,
                "kot": item.kot.kot_number if item.kot else "-",
                "course_number": item.course_number,
                "fire_status": item.get_fire_status_display(),
                "hold_until_time": item.hold_until_time.strftime("%H:%M") if item.hold_until_time else "-",
                "fired_by": item.fired_by.username if item.fired_by else "-",
                "fired_timestamp": item.fired_timestamp.isoformat() if item.fired_timestamp else "-",
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
