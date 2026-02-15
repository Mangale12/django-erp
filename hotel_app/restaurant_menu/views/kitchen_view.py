from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from hotel_app.restaurant_menu.models import Kitchen  # your Kitchen model


def index(request):
    """
    Render the main Kitchen list page
    """
    kitchens = Kitchen.objects.select_related("outlet").all()

    fields = [
        {"name": "kitchen_code", "label": "Code", "type": "text", "required": True},
        {"name": "kitchen_name", "label": "Name", "type": "text", "required": True},
        {"name": "kitchen_type", "label": "Type", "type": "select", "options": Kitchen.KitchenType.choices},
        {"name": "outlet", "label": "Outlet", "type": "select", "options": [(o.id, o.outlet_name) for o in Kitchen.objects.values_list('outlet__id', 'outlet__outlet_name').distinct()]},
        {"name": "is_kds_enabled", "label": "KDS Enabled", "type": "checkbox"},
        {"name": "is_printer_enabled", "label": "Printer Enabled", "type": "checkbox"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True},
    ]

    return render(request, 'restaurant_menu/kitchen/list.html', {
        'kitchens': kitchens,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    """
    Create Kitchen (normal POST or AJAX)
    """
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        try:
            with transaction.atomic():
                kitchen = Kitchen.objects.create(
                    kitchen_code=request.POST.get('kitchen_code'),
                    kitchen_name=request.POST.get('kitchen_name'),
                    kitchen_type=request.POST.get('kitchen_type'),
                    outlet_id=request.POST.get('outlet'),
                    printer_ip_address=request.POST.get('printer_ip_address'),
                    backup_printer_ip=request.POST.get('backup_printer_ip'),
                    kds_display_id=request.POST.get('kds_display_id'),
                    is_kds_enabled=bool(request.POST.get('is_kds_enabled')),
                    is_printer_enabled=bool(request.POST.get('is_printer_enabled')),
                    display_order=request.POST.get('display_order') or 1,
                    is_active=bool(request.POST.get('is_active')),
                    created_by=request.user
                )

                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Kitchen created successfully',
                        'kitchen': {
                            'id': kitchen.id,
                            'code': kitchen.kitchen_code,
                            'name': kitchen.kitchen_name,
                            'type': kitchen.get_kitchen_type_display(),
                            'edit_url': reverse('kitchen_update', args=[kitchen.id]),
                            'delete_url': reverse('kitchen_delete', args=[kitchen.id]),
                        }
                    })

                messages.success(request, 'Kitchen created successfully')
                return redirect('kitchen_list')

        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            messages.error(request, f'Error creating kitchen: {str(e)}')
            return redirect('kitchen_list')

    return render(request, 'restaurant_menu/kitchen/form.html')


def edit(request, pk):
    """
    Return kitchen data for AJAX edit
    """
    kitchen = get_object_or_404(Kitchen, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': kitchen.id,
            'kitchen_code': kitchen.kitchen_code,
            'kitchen_name': kitchen.kitchen_name,
            'kitchen_type': kitchen.kitchen_type,
            'outlet': kitchen.outlet.id,
            'printer_ip_address': kitchen.printer_ip_address,
            'backup_printer_ip': kitchen.backup_printer_ip,
            'kds_display_id': kitchen.kds_display_id,
            'is_kds_enabled': kitchen.is_kds_enabled,
            'is_printer_enabled': kitchen.is_printer_enabled,
            'display_order': kitchen.display_order,
            'is_active': kitchen.is_active,
        }
    }
    return JsonResponse(data)


@require_http_methods(["POST"])
def update_ajax(request, pk):
    """
    Update Kitchen via AJAX
    """
    kitchen = get_object_or_404(Kitchen, pk=pk)

    try:
        kitchen.kitchen_code = request.POST.get('kitchen_code')
        kitchen.kitchen_name = request.POST.get('kitchen_name')
        kitchen.kitchen_type = request.POST.get('kitchen_type')
        kitchen.outlet_id = request.POST.get('outlet')
        kitchen.printer_ip_address = request.POST.get('printer_ip_address')
        kitchen.backup_printer_ip = request.POST.get('backup_printer_ip')
        kitchen.kds_display_id = request.POST.get('kds_display_id')
        kitchen.is_kds_enabled = bool(request.POST.get('is_kds_enabled'))
        kitchen.is_printer_enabled = bool(request.POST.get('is_printer_enabled'))
        kitchen.display_order = request.POST.get('display_order') or 1
        kitchen.is_active = bool(request.POST.get('is_active'))
        kitchen.updated_by = request.user
        kitchen.save()

        return JsonResponse({
            'success': True,
            'message': 'Kitchen updated successfully',
            'kitchen': {
                'id': kitchen.id,
                'code': kitchen.kitchen_code,
                'name': kitchen.kitchen_name,
                'type': kitchen.get_kitchen_type_display(),
                'edit_url': reverse('kitchen_update', args=[kitchen.id]),
                'delete_url': reverse('kitchen_delete', args=[kitchen.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    """
    Delete Kitchen (normal or AJAX)
    """
    kitchen = get_object_or_404(Kitchen, pk=pk)
    kitchen.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Kitchen deleted successfully'})

    messages.success(request, 'Kitchen deleted successfully')
    return redirect('kitchen_list')


def datatable(request):
    """
    Server-side DataTable JSON
    """
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "")

    qs = Kitchen.objects.select_related("outlet")

    if search_value:
        qs = qs.filter(
            Q(kitchen_code__icontains=search_value) |
            Q(kitchen_name__icontains=search_value) |
            Q(outlet__outlet_name__icontains=search_value)
        )

    total_records = Kitchen.objects.count()
    filtered_records = qs.count()
    qs = qs[start:start + length]

    data = []
    for k in qs:
        data.append({
            "code": k.kitchen_code,
            "name": k.kitchen_name,
            "type": k.get_kitchen_type_display(),
            "outlet": k.outlet.outlet_name,
            "kds": "Yes" if k.is_kds_enabled else "No",
            "printer": k.printer_ip_address or "-",
            "status": "Active" if k.is_active else "Inactive",
            "actions": f"""
                <a href="{reverse('kitchen_update', args=[k.id])}" class="btn btn-sm btn-warning">Edit</a>
                <a href="{reverse('kitchen_delete', args=[k.id])}" class="btn btn-sm btn-danger">Delete</a>
            """
        })

    return JsonResponse({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data,
    })


def select(request):
    """
    Select2 AJAX endpoint
    """
    keyword = request.GET.get('term', '').strip()
    qs = Kitchen.objects.all()
    if keyword:
        qs = qs.filter(kitchen_name__icontains=keyword)

    qs = qs.order_by('-created_at')[:5]

    results = [{"id": k.id, "text": k.kitchen_name} for k in qs]
    return JsonResponse({"results": results})
