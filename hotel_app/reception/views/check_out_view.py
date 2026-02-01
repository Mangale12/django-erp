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
from hotel_app.reception.forms import CheckOutForm


def index(request):
    fields = [
        {"name": "guest", "label": "Guest", "type": "select", "required": True, "url": reverse('guest_select')},
        {"name": "room", "label": "Room", "type": "select", "required": True, "url": reverse('room_select')},
        {"name": "user", "label": "User", "type": "select", "required": True, "url": reverse('staff_select')},
        {"name" : "check_in", "label": "Check In", "type": "select", "required": True, "url": reverse('checkin_select')},
        {"name" : "check_out_time", "label": "Check Out Time", "type": "datetime", "required": True},
        {"name": "payment_mode", "label": "Payment Mode", "type": "select", "required": True, "url": reverse('payment_mode_select')},
        {"name": "late_check_out_charge", "label": "Late Check Out Charge", "type": "number", "required": True},
        {"name": "minibar_charge", "label": "Minibar Charge", "type": "number", "required": True},
        {"name": "damage_charge", "label": "Damage Charge", "type": "number", "required": True},
        {"name": "other_charge", "label": "Other Charge", "type": "number", "required": True},
        {"name": "final_bill_amount", "label": "Final Bill Amount", "type": "number", "required": True},
        {"name": "remarks", "label": "Remarks", "type": "textarea", "required": False},
    ] 
    return render(request, 'reception/check_out/index.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Use form.save() - it's cleaner and handles all fields automatically
                    check_in = form.save()
                
                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'Check Out created successfully'})
                
                messages.success(request, 'Check Out created successfully')
                return redirect('check_out_list')
            except Exception as e:
                if is_ajax:
                    return JsonResponse({'success': False, 'error': str(e)}, status=500)
                messages.error(request, f'Error: {str(e)}')
        else:
            # IMPORTANT: Handle validation errors
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            return render(request, 'reception/check_out/form.html', {'form': form})

    return render(request, 'reception/check_out/form.html', {'form': CheckOutForm()})



def edit(request, pk):
    """Return guest data as JSON"""
    check_out = get_object_or_404(CheckOut, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': check_out.id,
            'guest': check_out.guest,
            'room': check_out.room,
            'user': check_out.user,
            'check_in': check_out.check_in,
            'check_out_time': check_out.check_out_time,
            'late_check_out_charge': check_out.late_check_out_charge,
            'minibar_charge': check_out.minibar_charge,
            'damage_charge': check_out.damage_charge,
            'other_charge': check_out.other_charge,
            'final_bill_amount': check_out.final_bill_amount,
            'payment_mode': check_out.payment_mode,
            'remarks': check_out.remarks,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for guest"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    check_out = get_object_or_404(CheckOut, pk=pk)
    form = CheckOutForm(request.POST, instance=check_out)
    
    
    try:
        if form.is_valid():
            form.save()
            
        return JsonResponse({
            'success': True,
            'message': 'Check Out updated successfully',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    check_out = get_object_or_404(CheckOut, pk=pk)
    check_out.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Check Out deleted successfully'})
    
    messages.success(request, 'Check Out deleted successfully')
    return redirect('check_out_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = CheckOut.objects.all()

    if keyword:
        qs = qs.filter(
            Q(guest__first_name__icontains=keyword) |
            Q(guest__last_name__icontains=keyword)
        )

    qs = qs.order_by('-created_at')[:5]

    results = [
        {
            "id": item.id,
            "text": item.guest.first_name + ' ' + item.guest.last_name 
        }
        for item in qs
    ]

    return JsonResponse({
        "results": results
    }) 