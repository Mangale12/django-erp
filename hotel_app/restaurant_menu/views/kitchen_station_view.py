from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from hotel_app.restaurant_menu.models import Kitchen, KitchenStation  # your Kitchen model
from master_setup.models import Printer  # your Printer model

from django.contrib.auth.decorators import login_required


def index(request):
    """
    Render the main Kitchen list page
    """

    fields = [
        {"name": "kitchen", "label": "Kitchen", "type": "select", "url": reverse('kitchen_select'), "required": True},
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "printer", "label": "Printer", "type": "select", "url": reverse('printer_select')},
        {"name": "kds_display_id", "label": "KDS Display ID", "type": "text"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True},
    ]

    return render(request, 'restaurant_menu/kitchen_station/list.html', {
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
                kitchen = KitchenStation.objects.create(
                    kitchen=get_object_or_404(Kitchen, pk=request.POST.get('kitchen')),
                    name=request.POST.get('name'),
                    printer=get_object_or_404(Printer, pk=request.POST.get('printer')) if request.POST.get('printer') else None,
                    kds_display_id=request.POST.get('kds_display_id'),
                    is_active=bool(request.POST.get('is_active')),
                )

                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Kitchen created successfully',
                        'kitchen': {
                            'id': kitchen.id,
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

    return render(request, 'restaurant_menu/kitchen_station/form.html')


def edit(request, pk):
    """
    Return kitchen data for AJAX edit
    """
    kitchen = get_object_or_404(Kitchen, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': kitchen.id,
            'kitchen': kitchen.kitchen.id,
            'name': kitchen.name,
            'printer': kitchen.printer.id if kitchen.printer else None,
            'kds_display_id': kitchen.kds_display_id,
            'is_active': kitchen.is_active,
        }
    }
    return JsonResponse(data)


@require_http_methods(["POST"])
def update(request, pk):
    """
    Update Kitchen via AJAX
    """
    kitchen = get_object_or_404(KitchenStation, pk=pk)

    try:
        kitchen.kitchen = get_object_or_404(Kitchen, pk=request.POST.get('kitchen'))
        kitchen.name = request.POST.get('name')
        kitchen.printer = get_object_or_404(Printer, pk=request.POST.get('printer')) if request.POST.get('printer') else None
        kitchen.kds_display_id = request.POST.get('kds_display_id')
        kitchen.is_active = bool(request.POST.get('is_active'))
        kitchen.save()

        return JsonResponse({
            'success': True,
            'message': 'Kitchen updated successfully',
            'kitchen': {
                'id': kitchen.id,
                'kitchen': kitchen.kitchen.id,
                'name': kitchen.name,
                'printer': kitchen.printer.id if kitchen.printer else None,
                'kds_display_id': kitchen.kds_display_id,
                'is_active': kitchen.is_active,
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
    kitchen = get_object_or_404(KitchenStation, pk=pk)
    kitchen.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Kitchen deleted successfully'})

    messages.success(request, 'Kitchen deleted successfully')
    return redirect('kitchen_list')


def select(request):
    """
    Select2 AJAX endpoint
    """
    keyword = request.GET.get('term', '').strip()
    qs = KitchenStation.objects.all()
    if keyword:
        qs = qs.filter(name__icontains=keyword)

    qs = qs.order_by('-created_at')[:5]

    results = [{"id": k.id, "text": k.name} for k in qs]
    return JsonResponse({"results": results})
