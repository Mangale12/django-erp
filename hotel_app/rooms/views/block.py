from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from hotel_app.rooms.models import Block


def block_list(request):
    blocks = Block.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'rooms/block/list.html', {
        'blocks': blocks,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def block_create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                block = Block.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Block created successfully',
                        'block': {
                            'id': block.id,
                            'name': block.name,
                            'code': block.code,
                            'description': block.description,
                            'is_active': block.is_active,
                            'edit_url': reverse('block_update', args=[block.id]),
                            'delete_url': reverse('block_delete', args=[block.id]),
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


def block_update(request, pk):
    block = get_object_or_404(Block, pk=pk)

    if request.method == 'POST':
        block.name = request.POST.get('name')
        block.code = request.POST.get('code')
        block.description = request.POST.get('description')
        block.is_active = True if request.POST.get('is_active') else False
        block.save()

        messages.success(request, 'Block updated successfully')
        return redirect('block_list')

    return render(request, 'rooms/block/form.html', {
        'block': block
    })


def block_edit(request, pk):
    """Return room view type data as JSON"""
    block = get_object_or_404(Block, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': block.id,
            'name': block.name,
            'code': block.code,
            'description': block.description,
            'is_active': block.is_active,
        }
    }
    return JsonResponse(data)


def block_update_ajax(request, pk):
    """Handle AJAX updates for room view types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    block = get_object_or_404(Block, pk=pk)
    
    try:
        block.name = request.POST.get('name')
        block.code = request.POST.get('code')
        block.description = request.POST.get('description', '')
        block.is_active = bool(request.POST.get('is_active'))
        block.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Block updated successfully',
            'block': {
                'id': block.id,
                'name': block.name,
                'code': block.code,
                'description': block.description,
                'is_active': block.is_active,
                'edit_url': reverse('block_update', args=[block.id]),
                'delete_url': reverse('block_delete', args=[block.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def block_delete(request, pk):
    block = get_object_or_404(Block, pk=pk)
    block.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Block deleted successfully'})
    
    messages.success(request, 'Block deleted successfully')
    return redirect('block_list')


def block_select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = Block.objects.all()

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