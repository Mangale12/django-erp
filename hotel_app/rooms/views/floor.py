from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from hotel_app.rooms.models import Floor


def floor_list(request):
    floors = Floor.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'rooms/floor/list.html', {
        'floors': floors,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def floor_create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                floor = Floor.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Floor created successfully',
                        'floor': {
                            'id': floor.id,
                            'name': floor.name,
                            'code': floor.code,
                            'description': floor.description,
                            'is_active': floor.is_active,
                            'edit_url': reverse('floor_update', args=[floor.id]),
                            'delete_url': reverse('floor_delete', args=[floor.id]),
                        }
                    })
                
                messages.success(request, 'Room View Type created successfully')
                return redirect('room_view_type_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating room view type: {str(e)}')
            return redirect('room_view_type_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'rooms/room_view_type/form.html')


def floor_update(request, pk):
    floor = get_object_or_404(Floor, pk=pk)

    if request.method == 'POST':
        floor.name = request.POST.get('name')
        floor.code = request.POST.get('code')
        floor.description = request.POST.get('description')
        floor.is_active = True if request.POST.get('is_active') else False
        floor.save()

        messages.success(request, 'Floor updated successfully')
        return redirect('floor_list')

    return render(request, 'rooms/floor/form.html', {
        'floor': floor
    })


def floor_edit(request, pk):
    """Return room view type data as JSON"""
    floor = get_object_or_404(Floor, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': floor.id,
            'name': floor.name,
            'code': floor.code,
            'description': floor.description,
            'is_active': floor.is_active,
        }
    }
    return JsonResponse(data)


def floor_update_ajax(request, pk):
    """Handle AJAX updates for room view types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    floor = get_object_or_404(Floor, pk=pk)
    
    try:
        floor.name = request.POST.get('name')
        floor.code = request.POST.get('code')
        floor.description = request.POST.get('description', '')
        floor.is_active = bool(request.POST.get('is_active'))
        floor.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Floor updated successfully',
            'floor': {
                'id': floor.id,
                'name': floor.name,
                'code': floor.code,
                'description': floor.description,
                'is_active': floor.is_active,
                'edit_url': reverse('floor_update', args=[floor.id]),
                'delete_url': reverse('floor_delete', args=[floor.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def floor_delete(request, pk):
    floor = get_object_or_404(Floor, pk=pk)
    floor.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Floor deleted successfully'})
    
    messages.success(request, 'Floor deleted successfully')
    return redirect('floor_list')


def floor_select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = Floor.objects.all()

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