from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import TaxType


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "tax_rate", "label": "Tax Rate", "type": "number", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/tax_type.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                tax_type = TaxType.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    tax_rate=request.POST.get('tax_rate'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Tax Type created successfully',
                        'tax_type': {
                            'id': tax_type.id,
                            'name': tax_type.name,
                            'code': tax_type.code,
                            'tax_rate': tax_type.tax_rate,
                            'description': tax_type.description,
                            'is_active': tax_type.is_active,
                            'edit_url': reverse('tax_type_update', args=[tax_type.id]),
                            'delete_url': reverse('tax_type_delete', args=[tax_type.id]),
                        }
                    })
                
                messages.success(request, 'Tax Type created successfully')
                return redirect('tax_type_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating account type: {str(e)}')
            return redirect('account_type_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'rooms/room_view_type/form.html')


def edit(request, pk):
    """Return room view type data as JSON"""
    tax_type = get_object_or_404(TaxType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': tax_type.id,
            'name': tax_type.name,
            'code': tax_type.code,
            'tax_rate': tax_type.tax_rate,
            'description': tax_type.description,
            'is_active': tax_type.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for tax types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    tax_type = get_object_or_404(TaxType, pk=pk)
    
    try:
        tax_type.name = request.POST.get('name')
        tax_type.code = request.POST.get('code')
        tax_type.tax_rate = request.POST.get('tax_rate')
        tax_type.description = request.POST.get('description', '')
        tax_type.is_active = bool(request.POST.get('is_active'))
        tax_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Tax Type updated successfully',
            'tax_type': {
                'id': tax_type.id,
                'name': tax_type.name,
                'code': tax_type.code,
                'tax_rate': tax_type.tax_rate,
                'description': tax_type.description,
                'is_active': tax_type.is_active,
                'edit_url': reverse('tax_type_update', args=[tax_type.id]),
                'delete_url': reverse('tax_type_delete', args=[tax_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    tax_type = get_object_or_404(TaxType, pk=pk)
    tax_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Tax Type deleted successfully'})
    
    messages.success(request, 'Tax Type deleted successfully')
    return redirect('tax_type_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = TaxType.objects.all()

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