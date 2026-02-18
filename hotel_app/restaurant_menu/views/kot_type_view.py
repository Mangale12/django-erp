from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from hotel_app.restaurant_menu.models import KOTType


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'restaurant_menu/kot_type/list.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                kot_type = KOTType.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'KOT Type created successfully',
                        'kot_type': {
                            'id': kot_type.id,
                            'name': kot_type.name,
                            'code': kot_type.code,
                            'description': kot_type.description,
                            'is_active': kot_type.is_active,
                            'edit_url': reverse('kot_type_update', args=[kot_type.id]),
                            'delete_url': reverse('kot_type_delete', args=[kot_type.id]),
                        }
                    })
                
                messages.success(request, 'KOT Type created successfully')
                return redirect('kot_type_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating KOT Type: {str(e)}')
            return redirect('kot_type_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'restaurant_menu/kot_type/form.html')


def update(request, pk):
    kot_type = get_object_or_404(KOTType, pk=pk)

    if request.method == 'POST':
        kot_type.name = request.POST.get('name')
        kot_type.code = request.POST.get('code')
        kot_type.description = request.POST.get('description')
        kot_type.is_active = True if request.POST.get('is_active') else False
        kot_type.save()

        messages.success(request, 'KOT Type updated successfully')
        return redirect('kot_type_list')

    return render(request, 'restaurant_menu/kot_type/form.html', {
        'kot_type': kot_type
    })


def edit(request, pk):
    """Return menu category data as JSON"""
    kot_type = get_object_or_404(KOTType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': kot_type.id,
            'name': kot_type.name,
            'code': kot_type.code,
            'description': kot_type.description,
            'is_active': kot_type.is_active,
        }
    }
    return JsonResponse(data)


def update_ajax(request, pk):
    """Handle AJAX updates for menu categories"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    kot_type = get_object_or_404(KOTType, pk=pk)
    
    try:
        kot_type.name = request.POST.get('name')
        kot_type.code = request.POST.get('code')
        kot_type.description = request.POST.get('description', '')
        kot_type.is_active = bool(request.POST.get('is_active'))
        kot_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'KOT Type updated successfully',
            'kot_type': {
                'id': kot_type.id,
                'name': kot_type.name,
                'code': kot_type.code,
                'description': kot_type.description,
                'is_active': kot_type.is_active,
                'edit_url': reverse('kot_type_update', args=[kot_type.id]),
                'delete_url': reverse('kot_type_delete', args=[kot_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    kot_type = get_object_or_404(KOTType, pk=pk)
    kot_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'KOT Type deleted successfully'})
    
    messages.success(request, 'KOT Type deleted successfully')
    return redirect('kot_type_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = KOTType.objects.all()

    if keyword:
        qs = qs.filter(name__icontains=keyword)


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

