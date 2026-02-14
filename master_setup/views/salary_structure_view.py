from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import SalaryStructure


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "basic_salary", "label": "Basic Salary", "type": "text", "required": True},
        {"name": "hra", "label": "HRA", "type": "text", "required": True},
        {"name": "special_allowance", "label": "Special Allowance", "type": "text", "required": True},
        {"name": "medical_allowance", "label": "Medical Allowance", "type": "text", "required": True},
        {"name": "conveyance_allowance", "label": "Conveyance Allowance", "type": "text", "required": True},
        {"name": "tax", "label": "Tax", "type": "text", "required": True},
        {"name": "pf", "label": "PF", "type": "text", "required": True},
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
                salary_structure = SalaryStructure.objects.create(
                    name=request.POST.get('name'),
                    basic_salary=request.POST.get('basic_salary'),
                    hra=request.POST.get('hra'),
                    special_allowance=request.POST.get('special_allowance'),
                    medical_allowance=request.POST.get('medical_allowance'),
                    conveyance_allowance=request.POST.get('conveyance_allowance'),
                    tax=request.POST.get('tax'),
                    pf=request.POST.get('pf'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Salary Structure created successfully',
                    })
                
                messages.success(request, 'Salary Structure created successfully')
                return redirect('salary_structure_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating salary structure: {str(e)}')
            return redirect('salary_structure_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/salary_structure/form.html')


def edit(request, pk):
    """Return room view type data as JSON"""
    salary_structure = get_object_or_404(SalaryStructure, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': salary_structure.id,
            'name': salary_structure.name,
            'basic_salary': salary_structure.basic_salary,
            'hra': salary_structure.hra,
            'special_allowance': salary_structure.special_allowance,
            'medical_allowance': salary_structure.medical_allowance,
            'conveyance_allowance': salary_structure.conveyance_allowance,
            'tax': salary_structure.tax,
            'pf': salary_structure.pf,
            'is_active': salary_structure.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for payment modes"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    salary_structure = get_object_or_404(SalaryStructure, pk=pk)
    
    try:
        salary_structure.name = request.POST.get('name')
        salary_structure.basic_salary = request.POST.get('basic_salary')
        salary_structure.hra = request.POST.get('hra')
        salary_structure.special_allowance = request.POST.get('special_allowance')
        salary_structure.medical_allowance = request.POST.get('medical_allowance')
        salary_structure.conveyance_allowance = request.POST.get('conveyance_allowance')
        salary_structure.tax = request.POST.get('tax')
        salary_structure.pf = request.POST.get('pf')
        salary_structure.is_active = bool(request.POST.get('is_active'))
        salary_structure.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Salary Structure updated successfully'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    salary_structure = get_object_or_404(SalaryStructure, pk=pk)
    salary_structure.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Salary Structure deleted successfully'})
    
    messages.success(request, 'Salary Structure deleted successfully')
    return redirect('salary_structure_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = SalaryStructure.objects.all()

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