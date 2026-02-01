from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import Department


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/department.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                department = Department.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Department created successfully',
                        'department': {
                            'id': department.id,
                            'name': department.name,
                            'code': department.code,
                            'description': department.description,
                            'is_active': department.is_active,
                            'edit_url': reverse('department_update', args=[department.id]),
                            'delete_url': reverse('department_delete', args=[department.id]),
                        }
                    })
                
                messages.success(request, 'Department created successfully')
                return redirect('department_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating department: {str(e)}')
            return redirect('department_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/department/form.html')


def edit(request, pk):
    """Return room view type data as JSON"""
    department = get_object_or_404(Department, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': department.id,
            'name': department.name,
            'code': department.code,
            'description': department.description,
            'is_active': department.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for account types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    department = get_object_or_404(Department, pk=pk)
    
    try:
        department.name = request.POST.get('name')
        department.code = request.POST.get('code')
        department.description = request.POST.get('description', '')
        department.is_active = bool(request.POST.get('is_active'))
        department.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Department updated successfully',
            'department': {
                'id': department.id,
                'name': department.name,
                'code': department.code,
                'description': department.description,
                'is_active': department.is_active,
                'edit_url': reverse('department_update', args=[department.id]),
                'delete_url': reverse('department_delete', args=[department.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Department deleted successfully'})
    
    messages.success(request, 'Department deleted successfully')
    return redirect('department_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = Department.objects.all()

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