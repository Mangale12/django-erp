from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import Designation, Department


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "department", "label": "Department", "type": "select", "required": True, "url": reverse('department_select')},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/designation.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        department_id = request.POST.get('department')
        department = get_object_or_404(Department, id=department_id)
        try:
            with transaction.atomic():
                designation = Designation.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    department=department,
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Designation created successfully',
                    })
                
                messages.success(request, 'Designation created successfully')
                return redirect('designation_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating designation: {str(e)}')
            return redirect('designation_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/designation/form.html')


def edit(request, pk):
    """Return room view type data as JSON"""
    designation = get_object_or_404(Designation, pk=pk)
    return HttpResponse(pk)
    data = {
        'success': True,
        'data': {
            'id': designation.id,
            'name': designation.name,
            'code': designation.code,
            'department': designation.department,
            'is_active': designation.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for account types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    designation = get_object_or_404(Designation, pk=pk)
    
    try:
        designation.name = request.POST.get('name')
        designation.code = request.POST.get('code')
        designation.department = request.POST.get('department')
        designation.is_active = bool(request.POST.get('is_active'))
        designation.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Designation updated successfully',
            'designation': {
                'id': designation.id,
                'name': designation.name,
                'code': designation.code,
                'department': designation.department,
                'is_active': designation.is_active,
                'edit_url': reverse('designation_update', args=[designation.id]),
                'delete_url': reverse('designation_delete', args=[designation.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    designation = get_object_or_404(Designation, pk=pk)
    designation.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Designation deleted successfully'})
    
    messages.success(request, 'Designation deleted successfully')
    return redirect('designation_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = Designation.objects.all()

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
