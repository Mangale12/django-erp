from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from restaurant_menu.models import MenuItem

class MenuItemDataTable(View):
    def get(self, request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()

        # Start with base queryset + select_related to avoid N+1
        base_queryset = MenuItem.objects.select_related('menu_category')

        total_records = base_queryset.count()  # Total without search

        # Apply search across MenuItem and MenuCategory fields
        if search_value:
            base_queryset = base_queryset.filter(
                Q(name__icontains=search_value) |
                Q(code__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(menu_category__name__icontains=search_value)  # ← Search in related model
            )

        filtered_records = base_queryset.count()
        
        # Apply ordering (optional but recommended)
        order_column = request.GET.get('order[0][column]', '0')
        order_dir = request.GET.get('order[0][dir]', 'asc')
        
        columns = ['id', 'name', 'code', 'menu_category__name', 'description', 'is_active']
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
                "code": item.code,
                "menu_category": item.menu_category.name if item.menu_category else "-",  # ← Key change
                "description": item.description or "",
                'price': item.price,
                "is_active": item.is_active,
                # Optional: include category ID if needed for editing
                # "menu_category_id": item.menu_category_id,
            })

        return JsonResponse({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": data
        })