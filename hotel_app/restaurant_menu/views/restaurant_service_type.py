from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from restaurant_menu.models import RestaurantServiceType


def restaurant_service_type_list(request):
    restaurant_service_types = RestaurantServiceType.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'restaurant_menu/restaurant_service_type/list.html', {
        'restaurant_service_types': restaurant_service_types,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def restaurant_service_type_create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                restaurant_service_type = RestaurantServiceType.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Restaurant Service Type created successfully',
                        'restaurant_service_type': {
                            'id': restaurant_service_type.id,
                            'name': restaurant_service_type.name,
                            'code': restaurant_service_type.code,
                            'description': restaurant_service_type.description,
                            'is_active': restaurant_service_type.is_active,
                            'edit_url': reverse('restaurant_service_type_update', args=[restaurant_service_type.id]),
                            'delete_url': reverse('restaurant_service_type_delete', args=[restaurant_service_type.id]),
                        }
                    })
                
                messages.success(request, 'Restaurant Service Type created successfully')
                return redirect('restaurant_service_type_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating restaurant service type: {str(e)}')
            return redirect('restaurant_service_type_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'restaurant_menu/restaurant_service_type/form.html')


def restaurant_service_type_update(request, pk):
    restaurant_service_type = get_object_or_404(RestaurantServiceType, pk=pk)

    if request.method == 'POST':
        restaurant_service_type.name = request.POST.get('name')
        restaurant_service_type.code = request.POST.get('code')
        restaurant_service_type.description = request.POST.get('description')
        restaurant_service_type.is_active = True if request.POST.get('is_active') else False
        restaurant_service_type.save()

        messages.success(request, 'Restaurant Service Type updated successfully')
        return redirect('restaurant_service_type_list')

    return render(request, 'restaurant_menu/restaurant_service_type/form.html', {
        'restaurant_service_type': restaurant_service_type
    })


def restaurant_service_type_edit(request, pk):
    """Return restaurant service type data as JSON"""
    restaurant_service_type = get_object_or_404(RestaurantServiceType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': restaurant_service_type.id,
            'name': restaurant_service_type.name,
            'code': restaurant_service_type.code,
            'description': restaurant_service_type.description,
            'is_active': restaurant_service_type.is_active,
        }
    }
    return JsonResponse(data)


def restaurant_service_type_update_ajax(request, pk):
    """Handle AJAX updates for restaurant service types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    restaurant_service_type = get_object_or_404(RestaurantServiceType, pk=pk)
    
    try:
        restaurant_service_type.name = request.POST.get('name')
        restaurant_service_type.code = request.POST.get('code')
        restaurant_service_type.description = request.POST.get('description', '')
        restaurant_service_type.is_active = bool(request.POST.get('is_active'))
        restaurant_service_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Restaurant Service Type updated successfully',
            'restaurant_service_type': {
                'id': restaurant_service_type.id,
                'name': restaurant_service_type.name,
                'code': restaurant_service_type.code,
                'description': restaurant_service_type.description,
                'is_active': restaurant_service_type.is_active,
                'edit_url': reverse('restaurant_service_type_update', args=[restaurant_service_type.id]),
                'delete_url': reverse('restaurant_service_type_delete', args=[restaurant_service_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def restaurant_service_type_delete(request, pk):
    restaurant_service_type = get_object_or_404(RestaurantServiceType, pk=pk)
    restaurant_service_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Restaurant Service Type deleted successfully'})
    
    messages.success(request, 'Restaurant Service Type deleted successfully')
    return redirect('restaurant_service_type_list')
