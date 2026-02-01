from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from restaurant_menu.models import FoodType


def food_type_list(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'restaurant_menu/food_type/list.tml', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def food_type_create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                food_type = FoodType.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Block created successfully',
                        'block': {
                            'id': food_type.id,
                            'name': food_type.name,
                            'code': food_type.code,
                            'description': food_type.description,
                            'is_active': food_type.is_active,
                            'edit_url': reverse('food_type_update', args=[food_type.id]),
                            'delete_url': reverse('food_type_delete', args=[food_type.id]),
                        }
                    })
                
                messages.success(request, 'Food Type created successfully')
                return redirect('food_type_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating food type: {str(e)}')
            return redirect('food_type_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'restaurant_menu/food_type/form.html')


def food_type_update(request, pk):
    food_type = get_object_or_404(FoodType, pk=pk)

    if request.method == 'POST':
        food_type.name = request.POST.get('name')
        food_type.code = request.POST.get('code')
        food_type.description = request.POST.get('description')
        food_type.is_active = True if request.POST.get('is_active') else False
        food_type.save()

        messages.success(request, 'Food Type updated successfully')
        return redirect('food_type_list')

    return render(request, 'rooms/block/form.html', {
        'block': block
    })


def food_type_edit(request, pk):
    """Return food type data as JSON"""
    food_type = get_object_or_404(FoodType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': food_type.id,
            'name': food_type.name,
            'code': food_type.code,
            'description': food_type.description,
            'is_active': food_type.is_active,
        }
    }
    return JsonResponse(data)


def food_type_update_ajax(request, pk):
    """Handle AJAX updates for food types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    food_type = get_object_or_404(FoodType, pk=pk)
    
    try:
        food_type.name = request.POST.get('name')
        food_type.code = request.POST.get('code')
        food_type.description = request.POST.get('description', '')
        food_type.is_active = bool(request.POST.get('is_active'))
        food_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Food Type updated successfully',
            'food_type': {
                'id': food_type.id,
                'name': food_type.name,
                'code': food_type.code,
                'description': food_type.description,
                'is_active': food_type.is_active,
                'edit_url': reverse('food_type_update', args=[food_type.id]),
                'delete_url': reverse('food_type_delete', args=[food_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def food_type_delete(request, pk):
    food_type = get_object_or_404(FoodType, pk=pk)
    food_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Food Type deleted successfully'})
    
    messages.success(request, 'Food Type deleted successfully')
    return redirect('food_type_list')
