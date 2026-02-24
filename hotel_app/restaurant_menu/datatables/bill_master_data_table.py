from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from hotel_app.restaurant_menu.selectors.bill_selector import BillSelector


class BillMasterDataTable(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()

        base_queryset = BillSelector.get_all()
        total_records = base_queryset.count()

        if search_value:
            base_queryset = base_queryset.filter(
                Q(bill_no__icontains=search_value)
                | Q(guest__name__icontains=search_value)
                | Q(room__room_number__icontains=search_value)
                | Q(outlet__name__icontains=search_value)
                | Q(payment_status__icontains=search_value)
                | Q(bill_status__icontains=search_value)
            )

        filtered_records = base_queryset.count()
        paginated_queryset = base_queryset.order_by("-created_at")[start : start + length]

        data = [
            {
                "id": item.id,
                "bill_no": item.bill_no,
                "guest": item.guest.name if item.guest else "-",
                "room": item.room.room_number if item.room else "-",
                "outlet": item.outlet.name if item.outlet else "-",
                "grand_total": str(item.grand_total or 0),
                "payment_status": item.payment_status,
                "bill_status": item.bill_status,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
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
