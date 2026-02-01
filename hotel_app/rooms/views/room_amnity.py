from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from hotel_app.rooms.models import RoomAmnity


def room_amnity_list(request):
    room_amnities = RoomAmnity.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "chargeable", "label": "Chargeable", "type": "checkbox", "default": True},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'rooms/room_amnity/list.html', {
        'room_amnities': room_amnities,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def room_amnity_create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                room_amnity = RoomAmnity.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    chargeable=bool(request.POST.get('chargeable')),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Room Amnity created successfully',
                        'room_amnity': {
                            'id': room_amnity.id,
                            'name': room_amnity.name,
                            'code': room_amnity.code,
                            'description': room_amnity.description,
                            'chargeable': room_amnity.chargeable,
                            'is_active': room_amnity.is_active,
                            'edit_url': reverse('room_amnity_update', args=[room_amnity.id]),
                            'delete_url': reverse('room_amnity_delete', args=[room_amnity.id]),
                        }
                    })
                
                messages.success(request, 'Room Amnity created successfully')
                return redirect('room_amnity_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating room amnity: {str(e)}')
            return redirect('room_amnity_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'rooms/room_category/form.html')


def room_amnity_update(request, pk):
    room_amnity = get_object_or_404(RoomAmnity, pk=pk)

    if request.method == 'POST':
        room_amnity.name = request.POST.get('name')
        room_amnity.code = request.POST.get('code')
        room_amnity.description = request.POST.get('description')
        room_amnity.chargeable = True if request.POST.get('chargeable') else False
        room_amnity.is_active = True if request.POST.get('is_active') else False
        room_amnity.save()

        messages.success(request, 'Room Amnity updated successfully')
        return redirect('room_amnity_list')

    return render(request, 'rooms/room_amnity/form.html', {
        'room_amnity': room_amnity
    })


def room_amnity_json(request, pk):
    """Return room category data as JSON"""
    room_amnity = get_object_or_404(RoomAmnity, pk=pk)
    data = {
        'success': True,
        'room_amnity': {
            'id': room_amnity.id,
            'name': room_amnity.name,
            'code': room_amnity.code,
            'description': room_amnity.description,
            'chargeable': room_amnity.chargeable,
            'is_active': room_amnity.is_active,
            'edit_url': reverse('room_amnity_update', args=[room_amnity.id]),
            'delete_url': reverse('room_amnity_delete', args=[room_amnity.id]),
        }
    }
    return JsonResponse(data)

def room_amnity_edit(request, pk):
    """Return room category data as JSON"""
    room_amnity = get_object_or_404(RoomAmnity, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': room_amnity.id,
            'name': room_amnity.name,
            'code': room_amnity.code,
            'description': room_amnity.description,
            'chargeable': room_amnity.chargeable,
            'is_active': room_amnity.is_active,
        }
    }
    return JsonResponse(data)


def room_amnity_update_ajax(request, pk):
    """Handle AJAX updates for room categories"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    room_amnity = get_object_or_404(RoomAmnity, pk=pk)
    
    try:
        room_amnity.name = request.POST.get('name')
        room_amnity.code = request.POST.get('code')
        room_amnity.description = request.POST.get('description', '')
        room_amnity.is_active = bool(request.POST.get('is_active'))
        room_amnity.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Room Amnity updated successfully',
            'room_amnity': {
                'id': room_amnity.id,
                'name': room_amnity.name,
                'code': room_amnity.code,
                'description': room_amnity.description,
                'chargeable': room_amnity.chargeable,
                'is_active': room_amnity.is_active,
                'edit_url': reverse('room_amnity_update', args=[room_amnity.id]),
                'delete_url': reverse('room_amnity_delete', args=[room_amnity.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def room_amnity_delete(request, pk):
    room_amnity = get_object_or_404(RoomAmnity, pk=pk)
    room_amnity.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Room Amnity deleted successfully'})
    
    messages.success(request, 'Room Amnity deleted successfully')
    return redirect('room_amnity_list')

def room_amnity_select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = RoomAmnity.objects.all()

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