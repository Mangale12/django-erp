from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from hotel_app.rooms.models import RoomType


def room_type_list(request):
    room_types = RoomType.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {
            "name": "max_adults",
            "label": "Max Adults",
            "type": "number",
            "required": True,
            "min": 1,
            "col": 6  # half-width
        },
        {
            "name": "max_children",
            "label": "Max Children",
            "type": "number",
            "min": 0,
            "col": 6  # half-width
        },
        {
            "name": "default_rate",
            "label": "Default Rate",
            "type": "number",
            "step": "0.01",
            "min": 0,
            "prefix": "$",  # special: adds input group
            "col": 12
        },
        {"name": "description", "label": "Description", "type": "textarea", "col": 12},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'rooms/room_type/list.html', {
        'room_types': room_types,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def room_type_create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                room_type = RoomType.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    max_adults=request.POST.get('max_adults'),
                    max_children=request.POST.get('max_children') or 0,
                    default_rate=request.POST.get('default_rate'),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Room Type created successfully',
                        'room_type': {
                            'id': room_type.id,
                            'name': room_type.name,
                            'code': room_type.code,
                            'max_adults': room_type.max_adults,
                            'max_children': room_type.max_children,
                            'default_rate': str(room_type.default_rate) if room_type.default_rate else None,
                            'edit_url': reverse('room_type_update', args=[room_type.id]),
                            'delete_url': reverse('room_type_delete', args=[room_type.id]),
                        }
                    })
                
                messages.success(request, 'Room Type created successfully')
                return redirect('room_type_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating room type: {str(e)}')
            return redirect('room_type_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'rooms/room_type/form.html')


def room_type_update(request, pk):
    room_type = get_object_or_404(RoomType, pk=pk)

    if request.method == 'POST':
        room_type.name = request.POST.get('name')
        room_type.code = request.POST.get('code')
        room_type.description = request.POST.get('description')
        room_type.max_adults = request.POST.get('max_adults')
        room_type.max_children = request.POST.get('max_children')
        room_type.default_rate = request.POST.get('default_rate')
        room_type.is_active = True if request.POST.get('is_active') else False
        room_type.save()

        messages.success(request, 'Room Type updated successfully')
        return redirect('room_type_list')

    return render(request, 'rooms/room_type/form.html', {
        'room_type': room_type
    })


def room_type_edit(request, pk):
    """Return room type data as JSON"""
    room_type = get_object_or_404(RoomType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': room_type.id,
            'name': room_type.name,
            'code': room_type.code,
            'description': room_type.description,
            'max_adults': room_type.max_adults,
            'max_children': room_type.max_children,
            'default_rate': str(room_type.default_rate) if room_type.default_rate is not None else None,
            'is_active': room_type.is_active,
            'edit_url': reverse('room_type_update', args=[room_type.id]),
            'delete_url': reverse('room_type_delete', args=[room_type.id]),
        }
    }
    return JsonResponse(data)

def room_type_edit(request, pk):
    room_type = get_object_or_404(RoomType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': room_type.id,
            'name': room_type.name,
            'code': room_type.code,
            'description': room_type.description,
            'max_adults': room_type.max_adults,
            'max_children': room_type.max_children,
            'default_rate': room_type.default_rate,
        }
    }
    return JsonResponse(data)


def room_type_update_ajax(request, pk):
    """Handle AJAX updates for room types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    room_type = get_object_or_404(RoomType, pk=pk)
    
    try:
        room_type.name = request.POST.get('name')
        room_type.code = request.POST.get('code')
        room_type.description = request.POST.get('description', '')
        room_type.max_adults = request.POST.get('max_adults')
        room_type.max_children = request.POST.get('max_children', 0)
        room_type.default_rate = request.POST.get('default_rate')
        room_type.is_active = bool(request.POST.get('is_active'))
        room_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Room Type updated successfully',
            'room_type': {
                'id': room_type.id,
                'name': room_type.name,
                'code': room_type.code,
                'max_adults': room_type.max_adults,
                'max_children': room_type.max_children,
                'default_rate': str(room_type.default_rate) if room_type.default_rate else None,
                'is_active': room_type.is_active,
                'edit_url': reverse('room_type_update', args=[room_type.id]),
                'delete_url': reverse('room_type_delete', args=[room_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def room_type_delete(request, pk):
    room_type = get_object_or_404(RoomType, pk=pk)
    room_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Room Type deleted successfully'})
    
    messages.success(request, 'Room Type deleted successfully')
    return redirect('room_type_list')


def room_type_select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = RoomType.objects.all()

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