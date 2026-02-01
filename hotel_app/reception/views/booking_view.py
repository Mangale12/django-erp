from django.shortcuts import render, redirect, get_object_or_404, reverse,HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from django.db.models import Q
from hotel_app.reception.forms import BookingForm
from hotel_app.reception.models import Booking
from hotel_app.reception.forms.booking_form import BookingForm


def index(request):
    fields = [
        {"name": "guest", "label": "Guest", "type": "select", "required": True, "url": reverse('guest_select')},
        {"name": "booking_source", "label": "Booking Source", "type": "select", "required": True, "url": reverse('booking_source_select')},
        {"name": "booking_date", "label": "Booking Date", "type": "date", "required": True},
        {"name": "check_in_date", "label": "Check In Date", "type": "date", "required": True},
        {"name": "check_out_date", "label": "Check Out Date", "type": "date", "required": True},
        {"name": "package_type", "label": "Package Type", "type": "static_select", "required": True, "options": Booking.PACKAGE_TYPE},
        {"name": "room", "label": "Room", "type": "select", "required": True, "url": reverse('room_select')},
        {"name": "no_of_adults", "label": "Number of Adults", "type": "number", "required": True},
        {"name": "no_of_children", "label": "Number of Children", "type": "number", "required": True},
        {"name": "discount_type", "label": "Discount Type", "type": "select", "required": False, "url": reverse('discount_type_select')},
        {"name": "discount_amount", "label": "Discount Amount", "type": "number", "required": False},
        {"name": "special_request", "label": "Special Request", "type": "textarea", "required": False},
        {"name": "booking_status", "label": "Booking Status", "type": "text", "required": True},
        {"name": "remarks", "label": "Remarks", "type": "textarea", "required": False},
    ]
    return render(request, 'reception/booking/index.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Use form.save() - it's cleaner and handles all fields automatically
                    booking = form.save()
                
                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'Booking created successfully'})
                
                messages.success(request, 'Booking created successfully')
                return redirect('booking_list')
            except Exception as e:
                if is_ajax:
                    return JsonResponse({'success': False, 'error': str(e)}, status=500)
                messages.error(request, f'Error: {str(e)}')
        else:
            # IMPORTANT: Handle validation errors
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            return render(request, 'reception/booking/form.html', {'form': form})

    return render(request, 'reception/booking/form.html', {'form': BookingForm()})



def edit(request, pk):
    """Return guest data as JSON"""
    booking = get_object_or_404(Booking, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': booking.id,
            'guest': booking.guest,
            'booking_source': booking.booking_source,
            'booking_date': booking.booking_date,
            'check_in_date': booking.check_in_date,
            'check_out_date': booking.check_out_date,
            'room': booking.room,
            'no_of_adults': booking.no_of_adults,
            'no_of_children': booking.no_of_children,
            'package_type': booking.package_type,
            'discount_type': booking.discount_type,
            'discount_amount': booking.discount_amount,
            'special_request': booking.special_request,
            'booking_status': booking.booking_status,
            'remarks': guest.remarks,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for guest"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    booking = get_object_or_404(Booking, pk=pk)
    form = BookingForm(request.POST, instance=booking)
    
    
    try:
        if form.is_valid():
            form.save()
            
        return JsonResponse({
            'success': True,
            'message': 'Guest updated successfully',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Booking deleted successfully'})
    
    messages.success(request, 'Booking deleted successfully')
    return redirect('booking_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = Booking.objects.all()

    if keyword:
        qs = qs.filter(
            Q(guest__first_name__icontains=keyword) |
            Q(guest__last_name__icontains=keyword)
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