from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from hotel_app.restaurant_menu.models import Order

class OrderDataTable(View):
    def get(self, request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()

        # Start with base queryset + select_related to avoid N+1
        base_queryset = Order.objects.select_related('table', 'user', 'room')

        total_records = base_queryset.count()  # Total without search

        # Apply search across MenuItem and MenuCategory fields
        if search_value:
            base_queryset = base_queryset.filter(
                Q(table__name__icontains=search_value) |
                Q(guest_name__icontains=search_value) |
                Q(room__room_number__icontains=search_value) |
                Q(order_start_time__icontains=search_value) |
                Q(order_status__icontains=search_value)
            )

        filtered_records = base_queryset.count()
        
        # Apply ordering (optional but recommended)
        order_column = request.GET.get('order[0][column]', '0')
        order_dir = request.GET.get('order[0][dir]', 'asc')
        
        columns = ['id', 'table', 'guest_name', 'room', 'order_start_time', 'order_status']
        if order_column.isdigit() and int(order_column) < len(columns):
            order_field = columns[int(order_column)]
            if order_dir == 'desc':
                order_field = f'-{order_field}'
            base_queryset = base_queryset.order_by(order_field)

        # Apply pagination
        paginated_queryset = base_queryset[start:start + length]

        # Build data with menu_category name
        data = []
        for item in paginated_queryset:
            data.append({
                "id": item.id,
                "order_number": item.order_number,
                "table": item.table.name if item.table else "-",  # ← Key change
                "guest_name": item.guest_name,
                "room": item.room.room_number if item.room else "-",  # ← Key change
                "order_start_time": item.order_start_time,
                "order_status": item.order_status,
                "guest_count": item.guest_count,
            })

        return JsonResponse({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": data
        })