from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from hotel_app.restaurant_menu.models import Outlet


def index(request):
    outlets = Outlet.objects.all()

    fields = [
        {"name": "outlet_code", "label": "Outlet Code", "type": "text", "required": True},
        {"name": "outlet_name", "label": "Outlet Name", "type": "text", "required": True},
        {
            "name": "outlet_type",
            "label": "Outlet Type",
            "type": "static_select",
            "options": Outlet.OUTLET_TYPE_CHOICES
        },
        {"name": "location_description", "label": "Location", "type": "text"},
        {"name": "opening_time", "label": "Opening Time", "type": "time"},
        {"name": "closing_time", "label": "Closing Time", "type": "time"},
        {"name": "service_charge_percentage", "label": "Service Charge %", "type": "number"},
        {"name": "vat_percentage", "label": "VAT %", "type": "number"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True},
    ]

    return render(request, 'restaurant_menu/outlet/list.html', {
        'outlets': outlets,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        try:
            with transaction.atomic():
                outlet = Outlet.objects.create(
                    outlet_code=request.POST.get('outlet_code'),
                    outlet_name=request.POST.get('outlet_name'),
                    outlet_type=request.POST.get('outlet_type'),
                    location_description=request.POST.get('location_description'),
                    opening_time=request.POST.get('opening_time') or None,
                    closing_time=request.POST.get('closing_time') or None,
                    service_charge_percentage=request.POST.get('service_charge_percentage') or 0,
                    vat_percentage=request.POST.get('vat_percentage') or 0,
                    is_active=bool(request.POST.get('is_active')),
                )

                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Outlet created successfully',
                        'outlet': {
                            'id': outlet.id,
                            'outlet_code': outlet.outlet_code,
                            'outlet_name': outlet.outlet_name,
                            'outlet_type': outlet.outlet_type,
                            'is_active': outlet.is_active,
                            'edit_url': reverse('outlet_update', args=[outlet.id]),
                            'delete_url': reverse('outlet_delete', args=[outlet.id]),
                        }
                    })

                messages.success(request, 'Outlet created successfully')
                return redirect('outlet_list')

        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)

            messages.error(request, f'Error creating outlet: {str(e)}')
            return redirect('outlet_list')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    return render(request, 'restaurant_menu/outlet/form.html')


def update(request, pk):
    outlet = get_object_or_404(Outlet, pk=pk)

    if request.method == 'POST':
        outlet.outlet_code = request.POST.get('outlet_code')
        outlet.outlet_name = request.POST.get('outlet_name')
        outlet.outlet_type = request.POST.get('outlet_type')
        outlet.location_description = request.POST.get('location_description')
        outlet.opening_time = request.POST.get('opening_time') or None
        outlet.closing_time = request.POST.get('closing_time') or None
        outlet.service_charge_percentage = request.POST.get('service_charge_percentage') or 0
        outlet.vat_percentage = request.POST.get('vat_percentage') or 0
        outlet.is_active = True if request.POST.get('is_active') else False
        outlet.save()

        messages.success(request, 'Outlet updated successfully')
        return redirect('outlet_list')

    return render(request, 'restaurant_menu/outlet/form.html', {
        'outlet': outlet
    })


def edit(request, pk):
    outlet = get_object_or_404(Outlet, pk=pk)

    data = {
        'success': True,
        'data': {
            'id': outlet.id,
            'outlet_code': outlet.outlet_code,
            'outlet_name': outlet.outlet_name,
            'outlet_type': outlet.outlet_type,
            'location_description': outlet.location_description,
            'opening_time': outlet.opening_time,
            'closing_time': outlet.closing_time,
            'service_charge_percentage': outlet.service_charge_percentage,
            'vat_percentage': outlet.vat_percentage,
            'is_active': outlet.is_active,
        }
    }

    return JsonResponse(data)


def update_ajax(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

    outlet = get_object_or_404(Outlet, pk=pk)

    try:
        outlet.outlet_code = request.POST.get('outlet_code')
        outlet.outlet_name = request.POST.get('outlet_name')
        outlet.outlet_type = request.POST.get('outlet_type')
        outlet.location_description = request.POST.get('location_description')
        outlet.opening_time = request.POST.get('opening_time') or None
        outlet.closing_time = request.POST.get('closing_time') or None
        outlet.service_charge_percentage = request.POST.get('service_charge_percentage') or 0
        outlet.vat_percentage = request.POST.get('vat_percentage') or 0
        outlet.is_active = bool(request.POST.get('is_active'))
        outlet.save()

        return JsonResponse({
            'success': True,
            'message': 'Outlet updated successfully',
            'outlet': {
                'id': outlet.id,
                'outlet_code': outlet.outlet_code,
                'outlet_name': outlet.outlet_name,
                'outlet_type': outlet.outlet_type,
                'is_active': outlet.is_active,
                'edit_url': reverse('outlet_update', args=[outlet.id]),
                'delete_url': reverse('outlet_delete', args=[outlet.id]),
            }
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    outlet = get_object_or_404(Outlet, pk=pk)
    outlet.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Outlet deleted successfully'})

    messages.success(request, 'Outlet deleted successfully')
    return redirect('outlet_list')


def select(request):
    keyword = request.GET.get('term', '').strip()

    qs = Outlet.objects.all()

    if keyword:
        qs = qs.filter(outlet_name__icontains=keyword)

    qs = qs.order_by('-created_at')[:5]

    results = [
        {
            "id": item.id,
            "text": item.outlet_name
        }
        for item in qs
    ]

    return JsonResponse({
        "results": results
    })
