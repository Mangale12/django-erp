from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from hotel_app.restaurant_menu.models import Folio


class FolioDataTable(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()

        base_queryset = Folio.objects.select_related("stay", "stay__guest").all()
        total_records = base_queryset.count()

        if search_value:
            filters = Q(stay__guest__name__icontains=search_value) | Q(folio_status__icontains=search_value)
            if search_value.isdigit():
                filters |= Q(folio_id=int(search_value)) | Q(stay_id=int(search_value))
            base_queryset = base_queryset.filter(filters)

        filtered_records = base_queryset.count()
        paginated_queryset = base_queryset.order_by("-created_at")[start : start + length]

        data = [
            {
                "id": item.pk,
                "folio_id": item.pk,
                "stay_id": item.stay_id,
                "guest_name": getattr(item.stay.guest, "name", "-") if item.stay_id else "-",
                "total_debit": float(item.total_debit),
                "total_credit": float(item.total_credit),
                "balance_amount": float(item.balance_amount),
                "folio_status": item.folio_status,
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
