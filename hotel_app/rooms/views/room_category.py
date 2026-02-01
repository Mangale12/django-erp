from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from hotel_app.rooms.models import RoomCategory


def room_category_list(request):
    room_categories = RoomCategory.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'rooms/room_category/list.html', {
        'room_categories': room_categories,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def room_category_create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                room_category = RoomCategory.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Room Category created successfully',
                        'room_category': {
                            'id': room_category.id,
                            'name': room_category.name,
                            'code': room_category.code,
                            'description': room_category.description,
                            'is_active': room_category.is_active,
                            'edit_url': reverse('room_category_update', args=[room_category.id]),
                            'delete_url': reverse('room_category_delete', args=[room_category.id]),
                        }
                    })
                
                messages.success(request, 'Room Category created successfully')
                return redirect('room_category_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating room category: {str(e)}')
            return redirect('room_category_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'rooms/room_category/form.html')


def room_category_update(request, pk):
    room_category = get_object_or_404(RoomCategory, pk=pk)

    if request.method == 'POST':
        room_category.name = request.POST.get('name')
        room_category.code = request.POST.get('code')
        room_category.description = request.POST.get('description')
        room_category.is_active = True if request.POST.get('is_active') else False
        room_category.save()

        messages.success(request, 'Room Category updated successfully')
        return redirect('room_category_list')

    return render(request, 'rooms/room_category/form.html', {
        'room_category': room_category
    })


def room_category_json(request, pk):
    """Return room category data as JSON"""
    room_category = get_object_or_404(RoomCategory, pk=pk)
    data = {
        'success': True,
        'room_category': {
            'id': room_category.id,
            'name': room_category.name,
            'code': room_category.code,
            'description': room_category.description,
            'is_active': room_category.is_active,
            'edit_url': reverse('room_category_update', args=[room_category.id]),
            'delete_url': reverse('room_category_delete', args=[room_category.id]),
        }
    }
    return JsonResponse(data)

def room_category_edit(request, pk):
    """Return room category data as JSON"""
    room_category = get_object_or_404(RoomCategory, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': room_category.id,
            'name': room_category.name,
            'code': room_category.code,
            'description': room_category.description,
            'is_active': room_category.is_active,
        }
    }
    return JsonResponse(data)


def room_category_update_ajax(request, pk):
    """Handle AJAX updates for room categories"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    room_category = get_object_or_404(RoomCategory, pk=pk)
    
    try:
        room_category.name = request.POST.get('name')
        room_category.code = request.POST.get('code')
        room_category.description = request.POST.get('description', '')
        room_category.is_active = bool(request.POST.get('is_active'))
        room_category.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Room Category updated successfully',
            'room_category': {
                'id': room_category.id,
                'name': room_category.name,
                'code': room_category.code,
                'description': room_category.description,
                'is_active': room_category.is_active,
                'edit_url': reverse('room_category_update', args=[room_category.id]),
                'delete_url': reverse('room_category_delete', args=[room_category.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def room_category_delete(request, pk):
    room_category = get_object_or_404(RoomCategory, pk=pk)
    room_category.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Room Category deleted successfully'})
    
    messages.success(request, 'Room Category deleted successfully')
    return redirect('room_category_list')

def room_category_select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = RoomCategory.objects.all()

    if keyword:
        qs = qs.filter(
            Q(name__icontains=keyword)
        )

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