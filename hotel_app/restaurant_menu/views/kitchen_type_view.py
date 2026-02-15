from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from hotel_app.restaurant_menu.models import KitchenType


def index(request):
    kitchen_types = KitchenType.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'restaurant_menu/kitchen_type/list.html', {
        'kitchen_types': kitchen_types,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                kitchen_type = KitchenType.objects.create(
                    name=request.POST.get('name'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Kitchen Type created successfully',
                        'kitchen_type': {
                            'id': kitchen_type.id,
                            'name': kitchen_type.name,
                            'description': kitchen_type.description,
                            'is_active': kitchen_type.is_active,
                            'edit_url': reverse('kitchen_type_update', args=[kitchen_type.id]),
                            'delete_url': reverse('kitchen_type_delete', args=[kitchen_type.id]),
                        }
                    })
                
                messages.success(request, 'Kitchen Type created successfully')
                return redirect('kitchen_type_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating kitchen type: {str(e)}')
            return redirect('kitchen_type_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'restaurant_menu/kitchen_type/form.html')


def update(request, pk):
    kitchen_type = get_object_or_404(KitchenType, pk=pk)

    if request.method == 'POST':
        kitchen_type.name = request.POST.get('name')
        kitchen_type.description = request.POST.get('description')
        kitchen_type.is_active = True if request.POST.get('is_active') else False
        kitchen_type.save()

        messages.success(request, 'Kitchen Type updated successfully')
        return redirect('kitchen_type_list')

    return render(request, 'restaurant_menu/kitchen_type/form.html', {
        'kitchen_type': kitchen_type
    })


def edit(request, pk):
    """Return menu category data as JSON"""
    kitchen_type = get_object_or_404(KitchenType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': kitchen_type.id,
            'name': kitchen_type.name,
            'description': kitchen_type.description,
            'is_active': kitchen_type.is_active,
        }
    }
    return JsonResponse(data)


def update_ajax(request, pk):
    """Handle AJAX updates for menu categories"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    kitchen_type = get_object_or_404(KitchenType, pk=pk)
    
    try:
        kitchen_type.name = request.POST.get('name')
        kitchen_type.description = request.POST.get('description', '')
        kitchen_type.is_active = bool(request.POST.get('is_active'))
        kitchen_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Kitchen Type updated successfully',
            'kitchen_type': {
                'id': kitchen_type.id,
                'name': kitchen_type.name,
                'description': kitchen_type.description,
                'is_active': kitchen_type.is_active,
                'edit_url': reverse('kitchen_type_update', args=[kitchen_type.id]),
                'delete_url': reverse('kitchen_type_delete', args=[kitchen_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    kitchen_type = get_object_or_404(KitchenType, pk=pk)
    kitchen_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Kitchen Type deleted successfully'})
    
    messages.success(request, 'Kitchen Type deleted successfully')
    return redirect('kitchen_type_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = KitchenType.objects.all()

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

