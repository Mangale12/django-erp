from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import EmployeeType


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/employee_type.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                employee_type = EmployeeType.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Employee Type created successfully',
                        'employee_type': {
                            'id': employee_type.id,
                            'name': employee_type.name,
                            'code': employee_type.code,
                            'description': employee_type.description,
                            'is_active': employee_type.is_active,
                            'edit_url': reverse('employee_type_update', args=[employee_type.id]),
                            'delete_url': reverse('employee_type_delete', args=[employee_type.id]),
                        }
                    })
                
                messages.success(request, 'Employee Type created successfully')
                return redirect('employee_type_list')
                
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
    """Return employee type data as JSON"""
    employee_type = get_object_or_404(EmployeeType, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': employee_type.id,
            'name': employee_type.name,
            'code': employee_type.code,
            'description': employee_type.description,
            'is_active': employee_type.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for employee types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    employee_type = get_object_or_404(EmployeeType, pk=pk)
    
    try:
        employee_type.name = request.POST.get('name')
        employee_type.code = request.POST.get('code')
        employee_type.description = request.POST.get('description', '')
        employee_type.is_active = bool(request.POST.get('is_active'))
        employee_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Employee Type updated successfully',
            'employee_type': {
                'id': employee_type.id,
                'name': employee_type.name,
                'code': employee_type.code,
                'description': employee_type.description,
                'is_active': employee_type.is_active,
                'edit_url': reverse('employee_type_update', args=[employee_type.id]),
                'delete_url': reverse('employee_type_delete', args=[employee_type.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    employee_type = get_object_or_404(EmployeeType, pk=pk)
    employee_type.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Employee Type deleted successfully'})
    
    messages.success(request, 'Employee Type deleted successfully')
    return redirect('employee_type_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = EmployeeType.objects.all()

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