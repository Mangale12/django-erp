from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import Country


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "code_alpha3", "label": "Code Alpha3", "type": "text", "required": True},
        {"name": "phone_code", "label": "Phone Code", "type": "text", "required": True},
    ]
    return render(request, 'master_setup/country.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                country = Country.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    code_alpha3=request.POST.get('code_alpha3'),
                    phone_code=request.POST.get('phone_code'),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Country created successfully',
                        'country': {
                            'id': country.id,
                            'name': country.name,
                            'code': country.code,
                            'code_alpha3': country.code_alpha3,
                            'phone_code': country.phone_code,
                            'edit_url': reverse('country_update', args=[country.id]),
                            'delete_url': reverse('country_delete', args=[country.id]),
                        }
                    })
                
                messages.success(request, 'Country created successfully')
                return redirect('country_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating country: {str(e)}')
            return redirect('country_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/country/form.html')



def edit(request, pk):
    """Return room view type data as JSON"""
    country = get_object_or_404(Country, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': country.id,
            'name': country.name,
            'code': country.code,
            'code_alpha3': country.code_alpha3,
            'phone_code': country.phone_code,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for account types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    country = get_object_or_404(Country, pk=pk)
    
    try:
        country.name = request.POST.get('name')
        country.code = request.POST.get('code')
        country.code_alpha3 = request.POST.get('code_alpha3')
        country.phone_code = request.POST.get('phone_code')
        country.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Country updated successfully',
            'country': {
                'id': country.id,
                'name': country.name,
                'code': country.code,
                'code_alpha3': country.code_alpha3,
                'phone_code': country.phone_code,
                'edit_url': reverse('country_update', args=[country.id]),
                'delete_url': reverse('country_delete', args=[country.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    country = get_object_or_404(Country, pk=pk)
    country.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Country deleted successfully'})
    
    messages.success(request, 'Country deleted successfully')
    return redirect('country_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = Country.objects.all()

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