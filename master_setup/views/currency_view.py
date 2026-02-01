from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import Currency


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "symbol", "label": "Symbol", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/currency.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                currency = Currency.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    symbol=request.POST.get('symbol'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Currency created successfully',
                        'currency': {
                            'id': currency.id,
                            'name': currency.name,
                            'code': currency.code,
                            'symbol': currency.symbol,
                            'is_active': currency.is_active,
                            'edit_url': reverse('currency_update', args=[currency.id]),
                            'delete_url': reverse('currency_delete', args=[currency.id]),
                        }
                    })
                
                messages.success(request, 'Currency created successfully')
                return redirect('currency_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating currency: {str(e)}')
            return redirect('currency_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/currency/form.html')



def edit(request, pk):
    """Return room view type data as JSON"""
    currency = get_object_or_404(Currency, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': currency.id,
            'name': currency.name,
            'code': currency.code,
            'symbol': currency.symbol,
            'is_active': currency.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for account types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    currency = get_object_or_404(Currency, pk=pk)
    
    try:
        currency.name = request.POST.get('name')
        currency.code = request.POST.get('code')
        currency.symbol = request.POST.get('symbol', '')
        currency.is_active = bool(request.POST.get('is_active'))
        currency.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Currency updated successfully',
            'currency': {
                'id': currency.id,
                'name': currency.name,
                'code': currency.code,
                'symbol': currency.symbol,
                'is_active': currency.is_active,
                'edit_url': reverse('currency_update', args=[currency.id]),
                'delete_url': reverse('currency_delete', args=[currency.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    currency = get_object_or_404(Currency, pk=pk)
    currency.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Currency deleted successfully'})
    
    messages.success(request, 'Currency deleted successfully')
    return redirect('currency_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = Currency.objects.all()

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