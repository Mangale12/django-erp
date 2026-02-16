from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from hotel_app.restaurant_menu.models import Kitchen, KitchenType, Outlet  # your Kitchen model
from django.contrib.auth.decorators import login_required


def index(request):
    """
    Render the main Kitchen list page
    """
    kitchens = Kitchen.objects.select_related("outlet").all()

    fields = [
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "type", "label": "Type", "type": "select", "url": reverse('kitchen_type_select')},
        {"name": "outlet", "label": "Outlet", "type": "select", "url": reverse('outlet_select')},
        {"name": "is_kds_enabled", "label": "KDS Enabled", "type": "checkbox"},
        {"name": "is_printer_enabled", "label": "Printer Enabled", "type": "checkbox"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True},
    ]

    return render(request, 'restaurant_menu/kitchen/list.html', {
        'kitchens': kitchens,
        'fields': fields
    })

@login_required
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
                    code=request.POST.get('code'),
                    name=request.POST.get('name'),
                    type=get_object_or_404(KitchenType, pk=request.POST.get('type')),
                    outlet=get_object_or_404(Outlet, pk=request.POST.get('outlet')),
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
                            'code': kitchen.code,
                            'name': kitchen.name,
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
            'code': kitchen.code,
            'name': kitchen.name,
            'type': kitchen.type.id,
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
def update(request, pk):
    """
    Update Kitchen via AJAX
    """
    kitchen = get_object_or_404(Kitchen, pk=pk)

    try:
        kitchen.code = request.POST.get('code')
        kitchen.name = request.POST.get('name')
        kitchen.type = KitchenType.objects.get_or_404(pk=request.POST.get('type'))
        kitchen.outlet = Outlet.objects.get_or_404(pk=request.POST.get('outlet'))
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
                'code': kitchen.code,
                'name': kitchen.name,
                'type': kitchen.get_type_display(),
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
            Q(code__icontains=search_value) |
            Q(name__icontains=search_value) |
            Q(outlet__outlet_name__icontains=search_value)
        )

    total_records = Kitchen.objects.count()
    filtered_records = qs.count()
    qs = qs[start:start + length]

    data = []
    for k in qs:
        data.append({
            "code": k.code,
            "name": k.name,
            "type": k.get_type_display(),
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
        qs = qs.filter(name__icontains=keyword)

    qs = qs.order_by('-created_at')[:5]

    results = [{"id": k.id, "text": k.name} for k in qs]
    return JsonResponse({"results": results})
