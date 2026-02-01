from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from hotel_app.rooms.models import BedType


def bed_type_list(request):
    bed_types = BedType.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'rooms/bed_type/list.html', {
        'bed_types': bed_types,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def bed_type_create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                bed_type = BedType.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Bed Type created successfully',
                        'bed_type': {
                            'id': bed_type.id,
                            'name': bed_type.name,
                            'code': bed_type.code,
                            'description': bed_type.description,
                            'is_active': bed_type.is_active,
                            'edit_url': reverse('bed_type_update', args=[bed_type.id]),
                            'delete_url': reverse('bed_type_delete', args=[bed_type.id]),
                        }
                    })
                
                messages.success(request, 'Bed Type created successfully')
                return redirect('bed_type_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating bed type: {str(e)}')
            return redirect('bed_type_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'rooms/room_view_type/form.html')


def bed_type_update(request, pk):
    bed_type = get_object_or_404(BedType, pk=pk)

    if request.method == 'POST':
        bed_type.name = request.POST.get('name')
        bed_type.code = request.POST.get('code')
        bed_type.description = request.POST.get('description')
        bed_type.is_active = True if request.POST.get('is_active') else False
        bed_type.save()

        messages.success(request, 'Bed Type updated successfully')
        return redirect('bed_type_list')

    return render(request, 'rooms/bed_type/form.html', {
        'bed_type': bed_type
    })


def bed_type_edit(request, pk):
    """Return room view type data as JSON"""
    bed_type = get_object_or_404(BedType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': bed_type.id,
            'name': bed_type.name,
            'code': bed_type.code,
            'description': bed_type.description,
            'is_active': bed_type.is_active,
        }
    }
    return JsonResponse(data)


def bed_type_update_ajax(request, pk):
    """Handle AJAX updates for room view types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    bed_type = get_object_or_404(BedType, pk=pk)
    
    try:
        bed_type.name = request.POST.get('name')
        bed_type.code = request.POST.get('code')
        bed_type.description = request.POST.get('description', '')
        bed_type.is_active = bool(request.POST.get('is_active'))
        bed_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Bed Type updated successfully',
            'bed_type': {
                'id': bed_type.id,
                'name': bed_type.name,
                'code': bed_type.code,
                'description': bed_type.description,
                'is_active': bed_type.is_active,
                'edit_url': reverse('bed_type_update', args=[bed_type.id]),
                'delete_url': reverse('bed_type_delete', args=[bed_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def bed_type_delete(request, pk):
    bed_type = get_object_or_404(BedType, pk=pk)
    bed_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Bed Type deleted successfully'})
    
    messages.success(request, 'Bed Type deleted successfully')
    return redirect('bed_type_list')


def bed_type_select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = BedType.objects.all()

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