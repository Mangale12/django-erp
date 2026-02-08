from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from hotel_app.restaurant_menu.models import Zone

class ZoneDataTable(View):
    def get(self, request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()

        # Start with base queryset + select_related to avoid N+1
        base_queryset = Zone.objects

        total_records = base_queryset.count()  # Total without search

        # Apply search across MenuItem and MenuCategory fields
        if search_value:
            base_queryset = base_queryset.filter(
                Q(name__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(service_charge_percentage__icontains=search_value) |
                Q(is_active__icontains=search_value)
            )

        filtered_records = base_queryset.count()
        
        # Apply ordering (optional but recommended)
        order_column = request.GET.get('order[0][column]', '0')
        order_dir = request.GET.get('order[0][dir]', 'asc')
        
        columns = ['id', 'name', 'description', 'service_charge_percentage', 'is_active']
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
                "name": item.name,
                "description": item.description or "",
                "service_charge_percentage": item.service_charge_percentage,
                "is_active": item.is_active,
            })

        return JsonResponse({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": data
        })