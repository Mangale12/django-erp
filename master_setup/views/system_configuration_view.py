from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import ShiftType


def shift_type_list(request):
    shift_types = ShiftType.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "start_time", "label": "Start Time", "type": "time", "required": True},
        {"name": "end_time", "label": "End Time", "type": "time", "required": True},
        {"name": "break_duration", "label": "Break Duration", "type": "time", "required": True},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/shift_type/list.html', {
        'shift_types': shift_types,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def shift_type_create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                shift_type = ShiftType.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    start_time=request.POST.get('start_time'),
                    end_time=request.POST.get('end_time'),
                    break_duration=request.POST.get('break_duration'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Shift Type created successfully',
                        'shift_type': {
                            'id': shift_type.id,
                            'name': shift_type.name,
                            'code': shift_type.code,
                            'start_time': shift_type.start_time,
                            'end_time': shift_type.end_time,
                            'break_duration': shift_type.break_duration,
                            'is_active': shift_type.is_active,
                            'edit_url': reverse('shift_type_update', args=[shift_type.id]),
                            'delete_url': reverse('shift_type_delete', args=[shift_type.id]),
                        }
                    })
                
                messages.success(request, 'Shift Type created successfully')
                return redirect('shift_type_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating shift type: {str(e)}')
            return redirect('shift_type_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/shift_type/form.html')


def shift_type_update(request, pk):
    shift_type = get_object_or_404(ShiftType, pk=pk)

    if request.method == 'POST':
        shift_type.name = request.POST.get('name')
        shift_type.code = request.POST.get('code')
        shift_type.start_time = request.POST.get('start_time')
        shift_type.end_time = request.POST.get('end_time')
        shift_type.break_duration = request.POST.get('break_duration')
        shift_type.is_active = True if request.POST.get('is_active') else False
        shift_type.save()

        messages.success(request, 'Shift Type updated successfully')
        return redirect('shift_type_list')

    return render(request, 'master_setup/shift_type/form.html', {
        'shift_type': shift_type
    })


def shift_type_edit(request, pk):
    """Return room view type data as JSON"""
    shift_type = get_object_or_404(ShiftType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': shift_type.id,
            'name': shift_type.name,
            'code': shift_type.code,
            'start_time': shift_type.start_time,
            'end_time': shift_type.end_time,
            'break_duration': shift_type.break_duration,
            'is_active': shift_type.is_active,
        }
    }
    return JsonResponse(data)


def shift_type_update_ajax(request, pk):
    """Handle AJAX updates for account types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    shift_type = get_object_or_404(ShiftType, pk=pk)
    
    try:
        shift_type.name = request.POST.get('name')
        shift_type.code = request.POST.get('code')
        shift_type.start_time = request.POST.get('start_time')
        shift_type.end_time = request.POST.get('end_time')
        shift_type.break_duration = request.POST.get('break_duration')
        shift_type.is_active = bool(request.POST.get('is_active'))
        shift_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Shift Type updated successfully',
            'shift_type': {
                'id': shift_type.id,
                'name': shift_type.name,
                'code': shift_type.code,
                'start_time': shift_type.start_time,
                'end_time': shift_type.end_time,
                'break_duration': shift_type.break_duration,
                'is_active': shift_type.is_active,
                'edit_url': reverse('shift_type_update', args=[shift_type.id]),
                'delete_url': reverse('shift_type_delete', args=[shift_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def shift_type_delete(request, pk):
    shift_type = get_object_or_404(ShiftType, pk=pk)
    shift_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Shift Type deleted successfully'})
    
    messages.success(request, 'Shift Type deleted successfully')
    return redirect('shift_type_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = ShiftType.objects.all()

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
