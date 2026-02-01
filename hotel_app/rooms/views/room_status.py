from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from hotel_app.rooms.models import RoomStatus


def room_status_list(request):
    room_statuses = RoomStatus.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'rooms/room_status/list.html', {
        'room_statuses': room_statuses,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def room_status_create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                room_status = RoomStatus.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Room Status created successfully',
                        'room_status': {
                            'id': room_status.id,
                            'name': room_status.name,
                            'code': room_status.code,
                            'description': room_status.description,
                            'is_active': room_status.is_active,
                            'edit_url': reverse('room_status_update', args=[room_status.id]),
                            'delete_url': reverse('room_status_delete', args=[room_status.id]),
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


def room_status_update(request, pk):
    room_status = get_object_or_404(RoomStatus, pk=pk)

    if request.method == 'POST':
        room_status.name = request.POST.get('name')
        room_status.code = request.POST.get('code')
        room_status.description = request.POST.get('description')
        room_status.is_active = True if request.POST.get('is_active') else False
        room_status.save()

        messages.success(request, 'Room Status updated successfully')
        return redirect('room_status_list')

    return render(request, 'rooms/room_status/form.html', {
        'room_status': room_status
    })


def room_status_edit(request, pk):
    """Return room view type data as JSON"""
    room_status = get_object_or_404(RoomStatus, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': room_status.id,
            'name': room_status.name,
            'code': room_status.code,
            'description': room_status.description,
            'is_active': room_status.is_active,
        }
    }
    return JsonResponse(data)


def room_status_update_ajax(request, pk):
    """Handle AJAX updates for room view types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    room_status = get_object_or_404(RoomStatus, pk=pk)
    
    try:
        room_status.name = request.POST.get('name')
        room_status.code = request.POST.get('code')
        room_status.description = request.POST.get('description', '')
        room_status.is_active = bool(request.POST.get('is_active'))
        room_status.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Room Status updated successfully',
            'room_status': {
                'id': room_status.id,
                'name': room_status.name,
                'code': room_status.code,
                'description': room_status.description,
                'is_active': room_status.is_active,
                'edit_url': reverse('room_status_update', args=[room_status.id]),
                'delete_url': reverse('room_status_delete', args=[room_status.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def room_status_delete(request, pk):
    room_status = get_object_or_404(RoomStatus, pk=pk)
    room_status.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Room Status deleted successfully'})
    
    messages.success(request, 'Room Status deleted successfully')
    return redirect('room_status_list')

def room_status_select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = RoomStatus.objects.all()

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