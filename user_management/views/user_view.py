from django.shortcuts import render, redirect, get_object_or_404, reverse,HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from django.db.models import Q
from hotel_app.reception.forms import GuestForm
from hotel_app.reception.models import Guest
from hotel_app.reception.forms.guest_form import GuestForm
from django.contrib.auth.models import User

def index(request):
    fields = [
        # {"name": "name", "label": "Name", "type": "text", "required": True},
        # {"name": "gender", "label": "Gender", "type": "static_select", "required": True, "options": UserForm.GENDER_CHOICES},
        # {"name": "dob", "label": "Date of Birth", "type": "date", "required": True},
        # {"name": "age", "label": "Age", "type": "number", "required": True},
        # {"name": "country", "label": "Country", "type": "select", "required": True, "url": reverse('country_select')},
        # {"name": "state", "label": "State", "type": "text", "required": True},
        # {"name": "city", "label": "City", "type": "text", "required": True},
        {"name": "nationality", "label": "Nationality", "type": "text", "required": True},
        {"name": "id_proof_type", "label": "ID Proof Type", "type": "static_select", "required": True, "options": GuestForm.ID_PROOF_TYPE_CHOICES},
        {"name": "id_proof_number", "label": "ID Proof Number", "type": "text", "required": True},
        {"name": "phone", "label": "Phone", "type": "text", "required": True},
        {"name": "email", "label": "Email", "type": "email", "required": True},
        {"name": "address", "label": "Address", "type": "textarea", "required": True},
        {"name": "guest_type", "label": "Guest Type", "type": "text", "required": True},
        {"name": "remarks", "label": "Remarks", "type": "textarea", "required": True},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'reception/guest/index.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Use form.save() - it's cleaner and handles all fields automatically
                    guest = form.save()
                
                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'Guest created successfully'})
                
                messages.success(request, 'Guest created successfully')
                return redirect('guest_list')
            except Exception as e:
                if is_ajax:
                    return JsonResponse({'success': False, 'error': str(e)}, status=500)
                messages.error(request, f'Error: {str(e)}')
        else:
            # IMPORTANT: Handle validation errors
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            return render(request, 'reception/guest/form.html', {'form': form})

    return render(request, 'reception/guest/form.html', {'form': GuestForm()})



def edit(request, pk):
    """Return guest data as JSON"""
    guest = get_object_or_404(Guest, pk=pk)
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
    
    guest = get_object_or_404(Guest, pk=pk)
    form = GuestForm(request.POST, instance=guest)
    
    
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
    guest = get_object_or_404(Guest, pk=pk)
    guest.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Guest deleted successfully'})
    
    messages.success(request, 'Guest deleted successfully')
    return redirect('guest_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = Guest.objects.all()

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

def staff_select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = User.objects.all()

    if keyword:
        qs = qs.filter(
            Q(first_name__icontains=keyword) |
            Q(last_name__icontains=keyword)
        )   

    qs = qs.order_by('-first_name')[:5]

    results = [
        {
            "id": item.id,
            "text": item.first_name + ' ' + item.last_name 
        }
        for item in qs
    ]

    return JsonResponse({
        "results": results
    })