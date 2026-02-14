from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import DiscountType


def index(request):
    return HttpResponse("Discount Type List")
    discount_types = DiscountType.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "discount_type", "label": "Discount Type", "type": "text", "required": True},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/discount_type.html', {
        'discount_types': discount_types,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                discount_type = DiscountType.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    discount_type=request.POST.get('discount_type'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Discount Type created successfully',
                        'discount_type': {
                            'id': discount_type.id,
                            'name': discount_type.name,
                            'code': discount_type.code,
                            'description': discount_type.description,
                            'discount_type': discount_type.discount_type,
                            'is_active': discount_type.is_active,
                            'edit_url': reverse('discount_type_update', args=[discount_type.id]),
                            'delete_url': reverse('discount_type_delete', args=[discount_type.id]),
                        }
                    })
                
                messages.success(request, 'Discount Type created successfully')
                return redirect('discount_type_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating discount type: {str(e)}')
            return redirect('discount_type_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/discount_type/form.html')


def edit(request, pk):
    """Return room view type data as JSON"""
    discount_type = get_object_or_404(DiscountType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': discount_type.id,
            'name': discount_type.name,
            'code': discount_type.code,
            'description': discount_type.description,
            'discount_type': discount_type.discount_type,
            'is_active': discount_type.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for discount types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    discount_type = get_object_or_404(DiscountType, pk=pk)
    
    try:
        discount_type.name = request.POST.get('name')
        discount_type.code = request.POST.get('code')
        discount_type.description = request.POST.get('description', '')
        discount_type.discount_type = request.POST.get('discount_type')
        discount_type.is_active = bool(request.POST.get('is_active'))
        discount_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Discount Type updated successfully',
            'discount_type': {
                'id': discount_type.id,
                'name': discount_type.name,
                'code': discount_type.code,
                'description': discount_type.description,
                'discount_type': discount_type.discount_type,
                'is_active': discount_type.is_active,
                'edit_url': reverse('discount_type_update', args=[discount_type.id]),
                'delete_url': reverse('discount_type_delete', args=[discount_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    discount_type = get_object_or_404(DiscountType, pk=pk)
    discount_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Discount Type deleted successfully'})
    
    messages.success(request, 'Discount Type deleted successfully')
    return redirect('discount_type_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = DiscountType.objects.all()

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