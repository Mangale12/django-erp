from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from hotel_app.rooms.models import RoomViewType


def room_view_type_list(request):
    room_view_types = RoomViewType.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'rooms/room_view_type/list.html', {
        'room_view_types': room_view_types,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def room_view_type_create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                room_view_type = RoomViewType.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Room View Type created successfully',
                        'room_view_type': {
                            'id': room_view_type.id,
                            'name': room_view_type.name,
                            'code': room_view_type.code,
                            'description': room_view_type.description,
                            'is_active': room_view_type.is_active,
                            'edit_url': reverse('room_view_type_update', args=[room_view_type.id]),
                            'delete_url': reverse('room_view_type_delete', args=[room_view_type.id]),
                        }
                    })
                
                messages.success(request, 'Room View Type created successfully')
                return redirect('room_view_type_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating room view type: {str(e)}')
            return redirect('room_view_type_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'rooms/room_view_type/form.html')


def room_view_type_update(request, pk):
    room_view_type = get_object_or_404(RoomViewType, pk=pk)

    if request.method == 'POST':
        room_view_type.name = request.POST.get('name')
        room_view_type.code = request.POST.get('code')
        room_view_type.description = request.POST.get('description')
        room_view_type.is_active = True if request.POST.get('is_active') else False
        room_view_type.save()

        messages.success(request, 'Room View Type updated successfully')
        return redirect('room_view_type_list')

    return render(request, 'rooms/room_view_type/form.html', {
        'room_view_type': room_view_type
    })


def room_view_type_edit(request, pk):
    """Return room view type data as JSON"""
    room_view_type = get_object_or_404(RoomViewType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': room_view_type.id,
            'name': room_view_type.name,
            'code': room_view_type.code,
            'description': room_view_type.description,
            'is_active': room_view_type.is_active,
        }
    }
    return JsonResponse(data)


def room_view_type_update_ajax(request, pk):
    """Handle AJAX updates for room view types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    room_view_type = get_object_or_404(RoomViewType, pk=pk)
    
    try:
        room_view_type.name = request.POST.get('name')
        room_view_type.code = request.POST.get('code')
        room_view_type.description = request.POST.get('description', '')
        room_view_type.is_active = bool(request.POST.get('is_active'))
        room_view_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Room View Type updated successfully',
            'room_view_type': {
                'id': room_view_type.id,
                'name': room_view_type.name,
                'code': room_view_type.code,
                'description': room_view_type.description,
                'is_active': room_view_type.is_active,
                'edit_url': reverse('room_view_type_update', args=[room_view_type.id]),
                'delete_url': reverse('room_view_type_delete', args=[room_view_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def room_view_type_delete(request, pk):
    room_view_type = get_object_or_404(RoomViewType, pk=pk)
    room_view_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Room View Type deleted successfully'})
    
    messages.success(request, 'Room View Type deleted successfully')
    return redirect('room_view_type_list')


def room_view_type_select(request, pk):
    room_view_type = get_object_or_404(RoomViewType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': room_view_type.id,
            'name': room_view_type.name,
            'code': room_view_type.code,
            'description': room_view_type.description,
            'is_active': room_view_type.is_active,
        }
    }
    return JsonResponse(data)


def room_view_type_select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = RoomViewType.objects.all()

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