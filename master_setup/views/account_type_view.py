from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import AccountType


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/account_type.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                account_type = AccountType.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Account Type created successfully',
                        'account_type': {
                            'id': account_type.id,
                            'name': account_type.name,
                            'code': account_type.code,
                            'description': account_type.description,
                            'is_active': account_type.is_active,
                            'edit_url': reverse('account_type_update', args=[account_type.id]),
                            'delete_url': reverse('account_type_delete', args=[account_type.id]),
                        }
                    })
                
                messages.success(request, 'Account Type created successfully')
                return redirect('account_type_list')
                
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
    account_type = get_object_or_404(AccountType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': account_type.id,
            'name': account_type.name,
            'code': account_type.code,
            'description': account_type.description,
            'is_active': account_type.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for account types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    account_type = get_object_or_404(AccountType, pk=pk)
    
    try:
        account_type.name = request.POST.get('name')
        account_type.code = request.POST.get('code')
        account_type.description = request.POST.get('description', '')
        account_type.is_active = bool(request.POST.get('is_active'))
        account_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Account Type updated successfully',
            'account_type': {
                'id': account_type.id,
                'name': account_type.name,
                'code': account_type.code,
                'description': account_type.description,
                'is_active': account_type.is_active,
                'edit_url': reverse('account_type_update', args=[account_type.id]),
                'delete_url': reverse('account_type_delete', args=[account_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    account_type = get_object_or_404(AccountType, pk=pk)
    account_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Account Type deleted successfully'})
    
    messages.success(request, 'Account Type deleted successfully')
    return redirect('account_type_list')

def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = AccountType.objects.all()

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