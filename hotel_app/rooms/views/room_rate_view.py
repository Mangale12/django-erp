from django.shortcuts import render, redirect, get_object_or_404, reverse,HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from django.db.models import Q
from hotel_app.rooms.forms import RoomRateForm
from hotel_app.rooms.models import RoomRate


def room_rate_list(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "rate", "label": "Rate", "type": "number", "required": True},
        {"name": "capacity", "label": "Capacity", "type": "number", "required": True},
        {"name": "extra_bed_charge", "label": "Extra Bed Charge", "type": "number", "required": True},
        {"name": "tax_type", "label": "Tax Type", "type": "select", "required": True, "url" : reverse('tax_type_select')},
        {"name": "is_active", "label": "Is Active", "type": "checkbox", "required": False},
    ]
    return render(request, 'rooms/room_rate/index.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def room_rate_create(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == 'POST':
        form = RoomRateForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Use form.save() - it's cleaner and handles all fields automatically
                    room_rate = form.save()
                
                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'Room Rate created successfully'})
                
                messages.success(request, 'Room Rate created successfully')
                return redirect('room_rate_list')
            except Exception as e:
                if is_ajax:
                    return JsonResponse({'success': False, 'error': str(e)}, status=500)
                messages.error(request, f'Error: {str(e)}')
        else:
            # IMPORTANT: Handle validation errors
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            return render(request, 'reception/booking/form.html', {'form': form})

    return render(request, 'reception/booking/form.html', {'form': RoomRateForm()})



def room_rate_edit(request, pk):
    """Return guest data as JSON"""
    room_rate = get_object_or_404(RoomRate, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': room_rate.id,
            'name': room_rate.name,
            'code': room_rate.code,
            'rate': room_rate.rate,
            'capacity': room_rate.capacity,
            'extra_bed_charge': room_rate.extra_bed_charge,
            'tax_type': room_rate.tax_type,
            'is_active': room_rate.is_active,
        }
    }
    return JsonResponse(data)


def room_rate_update(request, pk):
    """Handle AJAX updates for room rate"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    room_rate = get_object_or_404(RoomRate, pk=pk)
    form = RoomRateForm(request.POST, instance=room_rate)
    
    
    try:
        if form.is_valid():
            form.save()
            
        return JsonResponse({
            'success': True,
            'message': 'Room Rate updated successfully',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def room_rate_delete(request, pk):
    room_rate = get_object_or_404(RoomRate, pk=pk)
    room_rate.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Room Rate deleted successfully'})
    
    messages.success(request, 'Room Rate deleted successfully')
    return redirect('room_rate_list')


def room_rate_select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = RoomRate.objects.all()

    if keyword:
        qs = qs.filter(
            Q(name__icontains=keyword) |
            Q(code__icontains=keyword)
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