from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from hotel_app.rooms.models import Room, RoomType, RoomCategory, Floor, RoomViewType, RoomAmnity


def room_list(request):
    rooms = Room.objects.all()
    fields = [
        {"name": "room_number", "label": "Room Number", "type": "text", "required": True},
        {"name": "room_type", "label": "Room Type", "type": "select", "required": True, "url" : reverse('room_type_select')},
        {"name": "room_category", "label": "Room Category", "type": "select", "required": True, "url" : reverse('room_category_select')},
        {"name": "floor", "label": "Floor", "type": "select", "required": True, "url" : reverse('floor_select')},
        {"name": "view_type", "label": "View Type", "type": "select", "required": True, "url" : reverse('room_view_type_select')},
        {"name": "amenities", "label": "Amenities", "type": "select", "required": True, "url" : reverse('room_amnity_select'), "attributes": {"multiple": True}},
        {"name": "current_status", "label": "Current Status", "type": "text", "required": True},
        {"name": "remarks", "label": "Remarks", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/room.html', {
        'rooms': rooms,
        'fields': fields
    })


@require_http_methods(["POST"])
def room_create(request):

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    try:
        with transaction.atomic():

            room = Room.objects.create(
                room_number=request.POST.get('room_number'),

                room_type=get_object_or_404(
                    RoomType, id=request.POST.get('room_type')
                ),

                room_category=get_object_or_404(
                    RoomCategory, id=request.POST.get('room_category')
                ),

                floor=get_object_or_404(
                    Floor, id=request.POST.get('floor')
                ),

                view_type=get_object_or_404(
                    RoomViewType, id=request.POST.get('view_type')
                ),

                current_status=request.POST.get('current_status'),
                remarks=request.POST.get('remarks'),
                is_active=bool(request.POST.get('is_active')),
            )

            # ✅ ManyToMany (amenities)
            amenities_ids = request.POST.getlist('amenities')
            if amenities_ids:
                room.amenities.set(amenities_ids)

        return JsonResponse({
            'success': True,
            'message': 'Room created successfully'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        room.room_number = request.POST.get('room_number')
        room.room_type = request.POST.get('room_type')
        room.room_category = request.POST.get('room_category')
        room.floor = request.POST.get('floor')
        room.view_type = request.POST.get('view_type')
        room.amenities = request.POST.get('amenities')
        room.current_status = request.POST.get('current_status')
        room.remarks = request.POST.get('remarks')
        room.is_active = True if request.POST.get('is_active') else False
        room.save()

        messages.success(request, 'Room updated successfully')
        return redirect('room_list')

    return render(request, 'rooms/room/form.html', {
        'room': room
    })


def room_edit(request, pk):
    """Return room data as JSON"""
    room = get_object_or_404(Room, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': room.id,
            'room_number': room.room_number,
            'room_type': room.room_type,
            'room_category': room.room_category,
            'floor': room.floor,
            'view_type': room.view_type,
            'amenities': room.amenities,
            'current_status': room.current_status,
            'remarks': room.remarks,
            'is_active': room.is_active,
        }
    }
    return JsonResponse(data)


def room_update_ajax(request, pk):
    """Handle AJAX updates for rooms"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    room = get_object_or_404(Room, pk=pk)
    
    try:
        room.room_number = request.POST.get('room_number')
        room.room_type = request.POST.get('room_type')
        room.room_category = request.POST.get('room_category')
        room.floor = request.POST.get('floor')
        room.view_type = request.POST.get('view_type')
        room.amenities = request.POST.get('amenities')
        room.current_status = request.POST.get('current_status')
        room.remarks = request.POST.get('remarks')
        room.is_active = bool(request.POST.get('is_active'))
        room.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Room updated successfully',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Room deleted successfully'})
    
    messages.success(request, 'Room deleted successfully')
    return redirect('room_list')


def room_select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = Room.objects.all()

    if keyword:
        qs = qs.filter(
            Q(room_number__icontains=keyword) |
            Q(room_type__icontains=keyword)
        )

    qs = qs.order_by('-created_at')[:5]

    results = [
        {
            "id": item.id,
            "text": item.room_number 
        }
        for item in qs
    ]

    return JsonResponse({
        "results": results
    })
    
