from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from hotel_app.restaurant_menu.models import Zone
from hotel_app.restaurant_menu.forms import ZoneForm


def index(request):
    zones = Zone.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "service_charge_percentage", "label": "Service Charge Percentage", "type": "number", "required": True},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'restaurant_menu/zone/list.html', {
        'zones': zones,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        try:
            with transaction.atomic():
                zone = Zone.objects.create(
                    name=request.POST.get('name'),
                    description=request.POST.get('description'),
                    service_charge_percentage=request.POST.get('service_charge_percentage'),
                    is_active=request.POST.get('is_active') == 'on',
                )

                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Zone created successfully',
                        'zone': {
                            'id': zone.id,
                            'name': zone.name,
                            'description': zone.description,
                            'service_charge_percentage': zone.service_charge_percentage,
                            'is_active': zone.is_active,
                            'edit_url': reverse('zone_update', args=[zone.id]),
                            'delete_url': reverse('zone_delete', args=[zone.id]),
                        }
                    })

                messages.success(request, 'Zone created successfully')
                return redirect('zone_list')

        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)

            messages.error(request, f'Error creating zone: {e}')
            return redirect('zone_list')

    # GET request
    return render(request, 'restaurant_menu/zone/form.html')


def update(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    if request.method == 'POST':
        zone.name = request.POST.get('name')
        zone.description = request.POST.get('description')
        zone.service_charge_percentage = request.POST.get('service_charge_percentage')
        zone.is_active = True if request.POST.get('is_active') else False
        zone.save()

        messages.success(request, 'Zone updated successfully')
        return redirect('zone_list')
    
    return render(request, 'restaurant_menu/zone/form.html', {
        'zone': zone
    })


def edit(request, pk):
    """Return zone data as JSON"""
    zone = get_object_or_404(Zone, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': zone.id,
            'name': zone.name,
            'description': zone.description,
            'service_charge_percentage': zone.service_charge_percentage,
            'is_active': zone.is_active,
        }
    }
    return JsonResponse(data)


def update_ajax(request, pk):
    """Handle AJAX updates for modifiers"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    zone = get_object_or_404(Zone, pk=pk)
    
    try:
        zone.name = request.POST.get('name')
        zone.description = request.POST.get('description', '')
        zone.service_charge_percentage = request.POST.get('service_charge_percentage')
        zone.is_active = bool(request.POST.get('is_active'))
        zone.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Zone updated successfully',
            'zone': {
                'id': zone.id,
                'name': zone.name,
                'description': zone.description,
                'service_charge_percentage': zone.service_charge_percentage,
                'is_active': zone.is_active,
                'edit_url': reverse('zone_update', args=[zone.id]),
                'delete_url': reverse('zone_delete', args=[zone.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    zone.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Zone deleted successfully'})
    
    messages.success(request, 'Zone deleted successfully')
    return redirect('zone_list')


def show(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    return render(request, 'restaurant_menu/zone/show.html', {
        'zone': zone
    })


def select(request):
    
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = Zone.objects.all()

    if keyword:
        qs = qs.filter(name__icontains=keyword)

    qs = qs.order_by('-created_at')[:5]

    results = [
        {
            "id": item.id,
            "text": item.name
        }
        for item in qs
    ]

    return JsonResponse({
        "results": results
    })

    