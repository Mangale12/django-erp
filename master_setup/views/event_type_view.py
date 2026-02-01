from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import EventType


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "text", "required": True},
        {"name" : "default_capacity", "label": "Default Capacity", "type": "number", "required": True},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/event_type.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                event_type = EventType.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    default_capacity=request.POST.get('default_capacity'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Event Type created successfully',
                        'event_type': {
                            'id': event_type.id,
                            'name': event_type.name,
                            'code': event_type.code,
                            'description': event_type.description,
                            'default_capacity': event_type.default_capacity,
                            'is_active': event_type.is_active,
                            'edit_url': reverse('event_type_update', args=[event_type.id]),
                            'delete_url': reverse('event_type_delete', args=[event_type.id]),
                        }
                    })
                
                messages.success(request, 'Event Type created successfully')
                return redirect('event_type_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating event type: {str(e)}')
            return redirect('event_type_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/event_type/form.html')


def edit(request, pk):
    """Return room view type data as JSON"""
    event_type = get_object_or_404(EventType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': event_type.id,
            'name': event_type.name,
            'code': event_type.code,
            'description': event_type.description,
            'default_capacity': event_type.default_capacity,
            'is_active': event_type.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for account types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    event_type = get_object_or_404(EventType, pk=pk)
    
    try:
        event_type.name = request.POST.get('name')
        event_type.code = request.POST.get('code')
        event_type.description = request.POST.get('description')
        event_type.default_capacity = request.POST.get('default_capacity')
        event_type.is_active = bool(request.POST.get('is_active'))
        event_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Event Type updated successfully',
            'event_type': {
                'id': event_type.id,
                'name': event_type.name,
                'code': event_type.code,
                'description': event_type.description,
                'default_capacity': event_type.default_capacity,
                'is_active': event_type.is_active,
                'edit_url': reverse('event_type_update', args=[event_type.id]),
                'delete_url': reverse('event_type_delete', args=[event_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    event_type = get_object_or_404(EventType, pk=pk)
    event_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Event Type deleted successfully'})
    
    messages.success(request, 'Event Type deleted successfully')
    return redirect('event_type_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = EventType.objects.all()

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
