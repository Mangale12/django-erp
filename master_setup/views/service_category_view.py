from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import ServiceCategory


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/service_category.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                service_category = ServiceCategory.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Service Category created successfully',
                        'service_category': {
                            'id': service_category.id,
                            'name': service_category.name,
                            'code': service_category.code,
                            'description': service_category.description,
                            'is_active': service_category.is_active,
                            'edit_url': reverse('service_category_update', args=[service_category.id]),
                            'delete_url': reverse('service_category_delete', args=[service_category.id]),
                        }
                    })
                
                messages.success(request, 'Service Category created successfully')
                return redirect('service_category_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating service category: {str(e)}')
            return redirect('service_category_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/service_category/form.html')


def edit(request, pk):
    """Return room view type data as JSON"""
    service_category = get_object_or_404(ServiceCategory, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': service_category.id,
            'name': service_category.name,
            'code': service_category.code,
            'description': service_category.description,
            'is_active': service_category.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for service categories"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    service_category = get_object_or_404(ServiceCategory, pk=pk)
    
    try:
        service_category.name = request.POST.get('name')
        service_category.code = request.POST.get('code')
        service_category.description = request.POST.get('description', '')
        service_category.is_active = bool(request.POST.get('is_active'))
        service_category.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Service Category updated successfully',
            'service_category': {
                'id': service_category.id,
                'name': service_category.name,
                'code': service_category.code,
                'description': service_category.description,
                'is_active': service_category.is_active,
                'edit_url': reverse('service_category_update', args=[service_category.id]),
                'delete_url': reverse('service_category_delete', args=[service_category.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    service_category = get_object_or_404(ServiceCategory, pk=pk)
    service_category.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Service Category deleted successfully'})
    
    messages.success(request, 'Service Category deleted successfully')
    return redirect('service_category_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = ServiceCategory.objects.all()

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