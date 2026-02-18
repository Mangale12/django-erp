from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from hotel_app.restaurant_menu.models import KOTStatus


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'restaurant_menu/kot_status/list.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                KOTStatus.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'KOT Status created successfully',
                    })
                
                messages.success(request, 'KOT Status created successfully')
                return redirect('kot_status_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating KOT Status: {str(e)}')
            return redirect('kot_status_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'restaurant_menu/kot_status/form.html')


def update(request, pk):
    kot_status = get_object_or_404(KOTStatus, pk=pk)

    if request.method == 'POST':
        kot_status.name = request.POST.get('name')
        kot_status.code = request.POST.get('code')
        kot_status.description = request.POST.get('description')
        kot_status.is_active = True if request.POST.get('is_active') else False
        kot_status.save()

        messages.success(request, 'KOT Status updated successfully')
        return redirect('kot_status_list')

    return render(request, 'restaurant_menu/kot_status/form.html', {
        'kot_status': kot_status
    })


def edit(request, pk):
    """Return menu category data as JSON"""
    kot_status = get_object_or_404(KOTStatus, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': kot_status.id,
            'name': kot_status.name,
            'code': kot_status.code,
            'description': kot_status.description,
            'is_active': kot_status.is_active,
        }
    }
    return JsonResponse(data)


def update_ajax(request, pk):
    """Handle AJAX updates for menu categories"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    kot_status = get_object_or_404(KOTStatus, pk=pk)
    
    try:
        kot_status.name = request.POST.get('name')
        kot_status.code = request.POST.get('code')
        kot_status.description = request.POST.get('description', '')
        kot_status.is_active = bool(request.POST.get('is_active'))
        kot_status.save()
        
        return JsonResponse({
            'success': True,
            'message': 'KOT Status updated successfully',
            'kot_status': {
                'id': kot_status.id,
                'name': kot_status.name,
                'code': kot_status.code,
                'description': kot_status.description,
                'is_active': kot_status.is_active,
                'edit_url': reverse('kot_status_update', args=[kot_status.id]),
                'delete_url': reverse('kot_status_delete', args=[kot_status.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    kot_status = get_object_or_404(KOTStatus, pk=pk)
    kot_status.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'KOT Status deleted successfully'})
    
    messages.success(request, 'KOT Status deleted successfully')
    return redirect('kot_status_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = KOTStatus.objects.all()

    if keyword:
        qs = qs.filter(name__icontains=keyword)

    qs = qs.order_by('-id')[:5]

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

