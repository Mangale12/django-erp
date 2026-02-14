from django.shortcuts import render, redirect, get_object_or_404, reverse,HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from django.db.models import Q
from hotel_app.reception.forms import CheckInForm
from hotel_app.reception.models import CheckIn
from hotel_app.reception.forms.checkin_form import CheckInForm


def index(request):
    fields = [
        {"name": "booking", "label": "Booking", "type": "select", "required": True, "url": reverse('booking_select')},
        {"name": "room", "label": "Room", "type": "select", "required": True, "url": reverse('room_select')},
        {"name" : "guest", "label": "Guest", "type": "select", "required": True, "url": reverse('guest_select')},
        {"name": "user", "label": "User", "type": "select", "required": True, "url": reverse('staff_select')},
        {"name": "payment_mode", "label": "Payment Mode", "type": "select", "required": True, "url": reverse('payment_mode_select')},
        {"name": "advance_amount", "label": "Advance Amount", "type": "number", "required": True},
        {"name": "check_in_time", "label": "Check In Time", "type": "datetime", "required": True},
        {"name": "remarks", "label": "Remarks", "type": "textarea", "required": False},
    ]
    return render(request, 'reception/checkin/index.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Use form.save() - it's cleaner and handles all fields automatically
                    check_in = form.save()
                
                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'Check In created successfully'})
                
                messages.success(request, 'Check In created successfully')
                return redirect('check_in_list')
            except Exception as e:
                if is_ajax:
                    return JsonResponse({'success': False, 'error': str(e)}, status=500)
                messages.error(request, f'Error: {str(e)}')
        else:
            # IMPORTANT: Handle validation errors
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            return render(request, 'reception/checkin/form.html', {'form': form})

    return render(request, 'reception/checkin/form.html', {'form': CheckInForm()})



def edit(request, pk):
    """Return guest data as JSON"""
    check_in = get_object_or_404(CheckIn, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': guest.id,
            'name': guest.name,
            'gender': guest.gender,
            'dob': guest.dob,
            'nationality': guest.nationality,
            'id_proof_type': guest.id_proof_type,
            'id_proof_number': guest.id_proof_number,
            'phone': guest.phone,
            'email': guest.email,
            'address': guest.address,
            'guest_type': guest.guest_type,
            'remarks': guest.remarks,
            'is_active': guest.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for guest"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    check_in = get_object_or_404(CheckIn, pk=pk)
    form = CheckInForm(request.POST, instance=check_in)
    
    
    try:
        if form.is_valid():
            form.save()
            
        return JsonResponse({
            'success': True,
            'message': 'Check In updated successfully',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    check_in = get_object_or_404(CheckIn, pk=pk)
    check_in.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Check In deleted successfully'})
    
    messages.success(request, 'Check In deleted successfully')
    return redirect('check_in_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = CheckIn.objects.all()

    if keyword:
        qs = qs.filter(
            Q(guest__name__icontains=keyword) |
            Q(guest__phone__icontains=keyword)
        )

    qs = qs.order_by('-created_at')[:5]

    results = [
        {
            "id": item.id,
            "text": item.guest.name
        }
        for item in qs
    ]

    return JsonResponse({
        "results": results
    })