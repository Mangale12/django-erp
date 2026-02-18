from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import PriorityLevel


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea", "required": True},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/priority_level.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                priority_level = PriorityLevel.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Priority Level created successfully',
                    })
                
                messages.success(request, 'Priority Level created successfully')
                return redirect('master_setup:priority_level_index')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating priority level: {str(e)}')
            return redirect('master_setup:priority_level_index')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/priority_level/form.html')


def edit(request, pk):
    """Return room view type data as JSON"""
    priority_level = get_object_or_404(PriorityLevel, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': priority_level.id,
            'name': priority_level.name,
            'code': priority_level.code,
            'description': priority_level.description,
            'is_active': priority_level.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for payment modes"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    priority_level = get_object_or_404(PriorityLevel, pk=pk)
    
    try:
        priority_level.name = request.POST.get('name')
        priority_level.code = request.POST.get('code')
        priority_level.description = request.POST.get('description')
        priority_level.is_active = request.POST.get('is_active')
        priority_level.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Priority Level updated successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def delete(request, pk):
    priority_level = get_object_or_404(PriorityLevel, pk=pk)
    priority_level.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Priority Level deleted successfully'})
    
    messages.success(request, 'Priority Level deleted successfully')
    return redirect('master_setup:priority_level_index')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = PriorityLevel.objects.all()

    if keyword:
        qs = qs.filter(name__icontains=keyword)

    qs = qs.order_by('-id')[:5]

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