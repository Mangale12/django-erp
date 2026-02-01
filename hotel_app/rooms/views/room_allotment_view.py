from django.shortcuts import render, redirect, get_object_or_404, reverse,HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from django.db.models import Q
from hotel_app.rooms.models import RoomAllotment
from hotel_app.rooms.forms import RoomAllotmentForm

def room_allotment_list(request):
    fields = [
        {"name": "booking", "label": "Booking", "type": "select", "required": True, "url": reverse('booking_select')},
        {"name": "room", "label": "Room", "type": "select", "required": True, "url": reverse('room_select')},
        {"name" : "alloted_by", "label": "Alloted By", "type": "select", "required": True, "url": reverse('staff_select')},
        {"name" : "alloted_at", "label": "Alloted At", "type": "datetime", "required": True},
       
    ] 
    return render(request, 'rooms/room_allotment/index.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def room_allotment_create(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == 'POST':
        form = RoomAllotmentForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Use form.save() - it's cleaner and handles all fields automatically
                    check_in = form.save()
                
                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'Check Out created successfully'})
                
                messages.success(request, 'Check Out created successfully')
                return redirect('room_allotment_list')
            except Exception as e:
                if is_ajax:
                    return JsonResponse({'success': False, 'error': str(e)}, status=500)
                messages.error(request, f'Error: {str(e)}')
        else:
            # IMPORTANT: Handle validation errors
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            return render(request, 'rooms/room_allotment/form.html', {'form': form})

    return render(request, 'rooms/room_allotment/form.html', {'form': RoomAllotmentForm()})



def room_allotment_edit(request, pk):
    """Return guest data as JSON"""
    room_allotment = get_object_or_404(RoomAllotment, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': room_allotment.id,
            'booking': room_allotment.booking,
            'room': room_allotment.room,
            'alloted_by': room_allotment.alloted_by,
            'alloted_at': room_allotment.alloted_at,
        }
    }
    return JsonResponse(data)


def room_allotment_update(request, pk):
    """Handle AJAX updates for guest"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    room_allotment = get_object_or_404(RoomAllotment, pk=pk)
    form = RoomAllotmentForm(request.POST, instance=room_allotment)
    
    
    try:
        if form.is_valid():
            form.save()
            
        return JsonResponse({
            'success': True,
            'message': 'Check Out updated successfully',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def room_allotment_delete(request, pk):
    room_allotment = get_object_or_404(RoomAllotment, pk=pk)
    room_allotment.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Room Allotment deleted successfully'})
    
    messages.success(request, 'Room Allotment deleted successfully')
    return redirect('room_allotment_list')


def room_allotment_select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = RoomAllotment.objects.all()

    if keyword:
        qs = qs.filter(
            Q(booking__guest__name__icontains=keyword)
        )

    qs = qs.order_by('-created_at')[:5]

    results = [
        {
            "id": item.id,
            "text": item.booking.booking_id + ' ' + item.booking.guest.name 
        }
        for item in qs
    ]

    return JsonResponse({
        "results": results
    }) 


def room_allotment_view(request, pk):
    room_allotment = get_object_or_404(RoomAllotment, pk=pk)
    return render(request, 'rooms/room_allotment/view.html', {'room_allotment': room_allotment})