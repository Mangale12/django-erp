from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import PaymentMode


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/payment_mode.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                payment_mode = PaymentMode.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Payment Mode created successfully',
                        'payment_mode': {
                            'id': payment_mode.id,
                            'name': payment_mode.name,
                            'code': payment_mode.code,
                            'description': payment_mode.description,
                            'is_active': payment_mode.is_active,
                            'edit_url': reverse('payment_mode_update', args=[payment_mode.id]),
                            'delete_url': reverse('payment_mode_delete', args=[payment_mode.id]),
                        }
                    })
                
                messages.success(request, 'Payment Mode created successfully')
                return redirect('payment_mode_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating payment mode: {str(e)}')
            return redirect('payment_mode_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/payment_mode/form.html')


def edit(request, pk):
    """Return room view type data as JSON"""
    payment_mode = get_object_or_404(PaymentMode, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': payment_mode.id,
            'name': payment_mode.name,
            'code': payment_mode.code,
            'description': payment_mode.description,
            'is_active': payment_mode.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for payment modes"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    payment_mode = get_object_or_404(PaymentMode, pk=pk)
    
    try:
        payment_mode.name = request.POST.get('name')
        payment_mode.code = request.POST.get('code')
        payment_mode.description = request.POST.get('description', '')
        payment_mode.is_active = bool(request.POST.get('is_active'))
        payment_mode.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Payment Mode updated successfully',
            'payment_mode': {
                'id': payment_mode.id,
                'name': payment_mode.name,
                'code': payment_mode.code,
                'description': payment_mode.description,
                'is_active': payment_mode.is_active,
                'edit_url': reverse('payment_mode_update', args=[payment_mode.id]),
                'delete_url': reverse('payment_mode_delete', args=[payment_mode.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    payment_mode = get_object_or_404(PaymentMode, pk=pk)
    payment_mode.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Payment Mode deleted successfully'})
    
    messages.success(request, 'Payment Mode deleted successfully')
    return redirect('payment_mode_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = PaymentMode.objects.all()

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