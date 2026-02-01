from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from master_setup.models import ShiftType

class ShiftTypeDataTable(View):
    def get(self, request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()

        base_queryset = ShiftType.objects.all()

        total_records = base_queryset.count()  # QUERY 1

        if search_value:
            base_queryset = base_queryset.filter(
                Q(name__icontains=search_value) |
                Q(code__icontains=search_value) |
                Q(start_time__icontains=search_value) |
                Q(end_time__icontains=search_value) |
                Q(break_duration__icontains=search_value)
            )

        filtered_records = base_queryset.count()  # QUERY 2

        paginated_queryset = base_queryset[start:start + length]  # QUERY 3

        data = [
            {
                "id": item.id,
                "name": item.name,
                "code": item.code,
                "start_time": item.start_time,
                "end_time": item.end_time,
                "break_duration": item.break_duration,
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
