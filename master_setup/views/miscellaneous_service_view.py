from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import MiscellaneousService


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "chargeable", "label": "Chargeable", "type": "checkbox", "required": True},
        {"name": "rate", "label": "Rate", "type": "number", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/miscellaneous_service.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                miscellaneous_service = MiscellaneousService.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    chargeable=bool(request.POST.get('chargeable')),
                    rate=request.POST.get('rate'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Miscellaneous Service created successfully',
                        'miscellaneous_service': {
                            'id': miscellaneous_service.id,
                            'name': miscellaneous_service.name,
                            'code': miscellaneous_service.code,
                            'chargeable': miscellaneous_service.chargeable,
                            'rate': miscellaneous_service.rate,
                            'description': miscellaneous_service.description,
                            'is_active': miscellaneous_service.is_active,
                            'edit_url': reverse('miscellaneous_service_update', args=[miscellaneous_service.id]),
                            'delete_url': reverse('miscellaneous_service_delete', args=[miscellaneous_service.id]),
                        }
                    })
                
                messages.success(request, 'Miscellaneous Service created successfully')
                return redirect('miscellaneous_service_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating miscellaneous service: {str(e)}')
            return redirect('miscellaneous_service_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/payment_mode/form.html')



def edit(request, pk):
    """Return room view type data as JSON"""
    miscellaneous_service = get_object_or_404(MiscellaneousService, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': miscellaneous_service.id,
            'name': miscellaneous_service.name,
            'code': miscellaneous_service.code,
            'chargeable': miscellaneous_service.chargeable,
            'rate': miscellaneous_service.rate,
            'description': miscellaneous_service.description,
            'is_active': miscellaneous_service.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for miscellaneous services"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    miscellaneous_service = get_object_or_404(MiscellaneousService, pk=pk)
    
    try:
        miscellaneous_service.name = request.POST.get('name')
        miscellaneous_service.code = request.POST.get('code')
        miscellaneous_service.chargeable = bool(request.POST.get('chargeable'))
        miscellaneous_service.rate = request.POST.get('rate')
        miscellaneous_service.description = request.POST.get('description', '')
        miscellaneous_service.is_active = bool(request.POST.get('is_active'))
        miscellaneous_service.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Miscellaneous Service updated successfully',
            'miscellaneous_service': {
                'id': miscellaneous_service.id,
                'name': miscellaneous_service.name,
                'code': miscellaneous_service.code,
                'chargeable': miscellaneous_service.chargeable,
                'rate': miscellaneous_service.rate,
                'description': miscellaneous_service.description,
                'is_active': miscellaneous_service.is_active,
                'edit_url': reverse('miscellaneous_service_update', args=[miscellaneous_service.id]),
                'delete_url': reverse('miscellaneous_service_delete', args=[miscellaneous_service.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    miscellaneous_service = get_object_or_404(MiscellaneousService, pk=pk)
    miscellaneous_service.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Miscellaneous Service deleted successfully'})
    
    messages.success(request, 'Miscellaneous Service deleted successfully')
    return redirect('miscellaneous_service_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = MiscellaneousService.objects.all()

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
