from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import ParkingType


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "text", "required": True},
        {"name" : "rate", "label": "Rate", "type": "number", "required": True},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/parking_type.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                parking_type = ParkingType.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    rate=request.POST.get('rate'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Parking Type created successfully',
                        'parking_type': {
                            'id': parking_type.id,
                            'name': parking_type.name,
                            'code': parking_type.code,
                            'description': parking_type.description,
                            'rate': parking_type.rate,
                            'is_active': parking_type.is_active,
                            'edit_url': reverse('parking_type_update', args=[parking_type.id]),
                            'delete_url': reverse('parking_type_delete', args=[parking_type.id]),
                        }
                    })
                
                messages.success(request, 'Parking Type created successfully')
                return redirect('parking_type_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating parking type: {str(e)}')
            return redirect('parking_type_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/parking_type/form.html')


def edit(request, pk):
    """Return room view type data as JSON"""
    parking_type = get_object_or_404(ParkingType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': parking_type.id,
            'name': parking_type.name,
            'code': parking_type.code,
            'description': parking_type.description,
            'rate': parking_type.rate,
            'is_active': parking_type.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for account types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    parking_type = get_object_or_404(ParkingType, pk=pk)
    
    try:
        parking_type.name = request.POST.get('name')
        parking_type.code = request.POST.get('code')
        parking_type.description = request.POST.get('description')
        parking_type.rate = request.POST.get('rate')
        parking_type.is_active = bool(request.POST.get('is_active'))
        parking_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Parking Type updated successfully',
            'parking_type': {
                'id': parking_type.id,
                'name': parking_type.name,
                'code': parking_type.code,
                'description': parking_type.description,
                'rate': parking_type.rate,
                'is_active': parking_type.is_active,
                'edit_url': reverse('parking_type_update', args=[parking_type.id]),
                'delete_url': reverse('parking_type_delete', args=[parking_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    parking_type = get_object_or_404(ParkingType, pk=pk)
    parking_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Parking Type deleted successfully'})
    
    messages.success(request, 'Parking Type deleted successfully')
    return redirect('parking_type_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = ParkingType.objects.all()

    if keyword:
        qs = qs.filter(name__icontains=keyword)

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
