from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from restaurant_menu.models import TableSetup


def table_setup_list(request):
    table_setups = TableSetup.objects.all()
    fields = [
        {"name": "table_name", "label": "Table Name", "type": "text", "required": True},
        {"name": "seating_capacity", "label": "Seating Capacity", "type": "number", "required": True},
        {"name": "location_area", "label": "Location Area", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'restaurant_menu/table_setup/list.html', {
        'table_setups': table_setups,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def table_setup_create(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        try:
            with transaction.atomic():
                table_setup = TableSetup.objects.create(
                    table_name=request.POST.get('table_name'),
                    seating_capacity=request.POST.get('seating_capacity'),
                    location_area=request.POST.get('location_area'),
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

def table_setup_update(request, pk):
    table_setup = get_object_or_404(TableSetup, pk=pk)

    if request.method == 'POST':
        table_setup.table_name = request.POST.get('table_name')
        table_setup.seating_capacity = request.POST.get('seating_capacity')
        table_setup.location_area = request.POST.get('location_area')
        table_setup.is_active = True if request.POST.get('is_active') else False
        table_setup.save()

        messages.success(request, 'Table Setup updated successfully')
        return redirect('table_setup_list')

    return render(request, 'restaurant_menu/table_setup/form.html', {
        'table_setup': table_setup
    })


def table_setup_edit(request, pk):
    """Return table setup data as JSON"""
    table_setup = get_object_or_404(TableSetup, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': table_setup.id,
            'table_name': table_setup.table_name,
            'seating_capacity': table_setup.seating_capacity,
            'location_area': table_setup.location_area,
            'is_active': table_setup.is_active,
        }
    }
    return JsonResponse(data)


def table_setup_update_ajax(request, pk):
    """Handle AJAX updates for table setups"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    table_setup = get_object_or_404(TableSetup, pk=pk)
    
    try:
        table_setup.table_name = request.POST.get('table_name')
        table_setup.seating_capacity = request.POST.get('seating_capacity')
        table_setup.location_area = request.POST.get('location_area')
        table_setup.is_active = bool(request.POST.get('is_active'))
        table_setup.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Table Setup updated successfully',
            'table_setup': {
                'id': table_setup.id,
                'table_name': table_setup.table_name,
                'seating_capacity': table_setup.seating_capacity,
                'location_area': table_setup.location_area,
                'is_active': table_setup.is_active,
                'edit_url': reverse('table_setup_update', args=[table_setup.id]),
                'delete_url': reverse('table_setup_delete', args=[table_setup.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def table_setup_delete(request, pk):
    table_setup = get_object_or_404(TableSetup, pk=pk)
    table_setup.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Table Setup deleted successfully'})
    
    messages.success(request, 'Table Setup deleted successfully')
    return redirect('table_setup_list')
