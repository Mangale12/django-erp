from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from hotel_app.restaurant_menu.models import FolioTransaction


class FolioTransactionDataTable(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()

        base_queryset = FolioTransaction.objects.select_related("folio", "folio__stay", "folio__stay__guest").all()
        total_records = base_queryset.count()

        if search_value:
            filters = Q(source_module_id__icontains=search_value)
            if search_value.isdigit():
                numeric_value = int(search_value)
                filters |= (
                    Q(folio_trn_id=numeric_value)
                    | Q(folio_id=numeric_value)
                    | Q(reference_id=numeric_value)
                    | Q(folio__stay_id=numeric_value)
                )
            base_queryset = base_queryset.filter(filters)

        filtered_records = base_queryset.count()
        paginated_queryset = base_queryset.order_by("-transaction_date")[start : start + length]

        data = [
            {
                "id": item.pk,
                "folio_trn_id": item.pk,
                "folio_id": item.folio_id,
                "stay_id": item.folio.stay_id,
                "source_module_id": item.source_module_id,
                "reference_id": item.reference_id,
                "debit_amount": float(item.debit_amount),
                "credit_amount": float(item.credit_amount),
                "transaction_date": item.transaction_date,
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
