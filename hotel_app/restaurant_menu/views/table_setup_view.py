from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from hotel_app.restaurant_menu.models import TableSetup, Zone


def index(request):
    table_setups = TableSetup.objects.all()
    fields = [
        {"name": "name", "label": "Table Name", "type": "text", "required": True},
        {"name": "seating_capacity", "label": "Seating Capacity", "type": "number", "required": True},
        {"name": "location_area", "label": "Location Area", "type": "textarea"},
        {"name": "zone", "label": "Zone", "type": "select", "required": True, "url": reverse('zone_select')},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'restaurant_menu/table_setup/list.html', {
        'table_setups': table_setups,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        try:
            with transaction.atomic():
                zone = Zone.objects.get(id=request.POST.get('zone'))
                table_setup = TableSetup.objects.create(
                    name=request.POST.get('name'),
                    seating_capacity=request.POST.get('seating_capacity'),
                    location_area=request.POST.get('location_area'),
                    zone=zone,
                    is_active='is_active' in request.POST,
                )

                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Table Setup created successfully',
                    })

                messages.success(request, 'Table Setup created successfully')
                return redirect('table_setup_list')

        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)

            messages.error(request, f'Error creating table setup: {str(e)}')
            return redirect('table_setup_list')

    # GET
    if is_ajax:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    return render(request, 'restaurant_menu/table_setup/form.html')

def update(request, pk):
    table_setup = get_object_or_404(TableSetup, pk=pk)

    if request.method == 'POST':
        table_setup.name = request.POST.get('name')
        table_setup.seating_capacity = request.POST.get('seating_capacity')
        table_setup.location_area = request.POST.get('location_area')
        zone = Zone.objects.get(id=request.POST.get('zone'))
        table_setup.zone = zone
        table_setup.is_active = True if request.POST.get('is_active') else False
        table_setup.save()

        messages.success(request, 'Table Setup updated successfully')
        return redirect('table_setup_list')

    return render(request, 'restaurant_menu/table_setup/form.html', {
        'table_setup': table_setup
    })


def edit(request, pk):
    """Return table setup data as JSON"""
    table_setup = get_object_or_404(TableSetup, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': table_setup.id,
            'name': table_setup.name,
            'seating_capacity': table_setup.seating_capacity,
            'location_area': table_setup.location_area,
            'zone': table_setup.zone.id,
            'is_active': table_setup.is_active,
        }
    }
    return JsonResponse(data)


def update_ajax(request, pk):
    """Handle AJAX updates for table setups"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    table_setup = get_object_or_404(TableSetup, pk=pk)
    
    try:
        table_setup.name = request.POST.get('name')
        table_setup.seating_capacity = request.POST.get('seating_capacity')
        table_setup.location_area = request.POST.get('location_area')
        zone = Zone.objects.get(id=request.POST.get('zone'))
        table_setup.zone = zone
        table_setup.is_active = bool(request.POST.get('is_active'))
        table_setup.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Table Setup updated successfully',
            'table_setup': {
                'id': table_setup.id,
                'name': table_setup.name,
                'seating_capacity': table_setup.seating_capacity,
                'location_area': table_setup.location_area,
                'zone': table_setup.zone.id,
                'is_active': table_setup.is_active,
                'edit_url': reverse('table_setup_update', args=[table_setup.id]),
                'delete_url': reverse('table_setup_delete', args=[table_setup.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    table_setup = get_object_or_404(TableSetup, pk=pk)
    table_setup.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Table Setup deleted successfully'})
    
    messages.success(request, 'Table Setup deleted successfully')
    return redirect('table_setup_list')

def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = TableSetup.objects.all()

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
    