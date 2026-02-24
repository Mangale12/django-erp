from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from master_setup.models import FiscalYear


class FiscalYearDataTable(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()

        base_queryset = FiscalYear.objects.all()
        total_records = base_queryset.count()

        if search_value:
            base_queryset = base_queryset.filter(
                Q(fiscal_year_name__icontains=search_value)
                | Q(description__icontains=search_value)
            )

        filtered_records = base_queryset.count()
        paginated_queryset = base_queryset[start : start + length]

        data = [
            {
                "id": item.id,
                "fiscal_year_name": item.fiscal_year_name,
                "start_date": item.start_date,
                "end_date": item.end_date,
                "description": item.description,
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
