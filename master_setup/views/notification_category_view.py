from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import NotificationCategory


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "text", "required": True},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/notification_category.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                notification_category = NotificationCategory.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Notification Category created successfully',
                        'notification_category': {
                            'id': notification_category.id,
                            'name': notification_category.name,
                            'code': notification_category.code,
                            'description': notification_category.description,
                            'is_active': notification_category.is_active,
                            'edit_url': reverse('notification_category_update', args=[notification_category.id]),
                            'delete_url': reverse('notification_category_delete', args=[notification_category.id]),
                        }
                    })
                
                messages.success(request, 'Notification Category created successfully')
                return redirect('notification_category_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating notification category: {str(e)}')
            return redirect('notification_category_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/notification_category/form.html')


def update(request, pk):
    notification_category = get_object_or_404(NotificationCategory, pk=pk)

    if request.method == 'POST':
        notification_category.name = request.POST.get('name')
        notification_category.code = request.POST.get('code')
        notification_category.description = request.POST.get('description')
        notification_category.is_active = True if request.POST.get('is_active') else False
        notification_category.save()

        messages.success(request, 'Notification Category updated successfully')
        return redirect('notification_category_list')

    return render(request, 'master_setup/notification_category/form.html', {
        'notification_category': notification_category
    })


def edit(request, pk):
    """Return room view type data as JSON"""
    notification_category = get_object_or_404(NotificationCategory, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': notification_category.id,
            'name': notification_category.name,
            'code': notification_category.code,
            'description': notification_category.description,
            'is_active': notification_category.is_active,
        }
    }
    return JsonResponse(data)


def update_ajax(request, pk):
    """Handle AJAX updates for account types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    notification_category = get_object_or_404(NotificationCategory, pk=pk)
    
    try:
        notification_category.name = request.POST.get('name')
        notification_category.code = request.POST.get('code')
        notification_category.description = request.POST.get('description')
        notification_category.is_active = bool(request.POST.get('is_active'))
        notification_category.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Notification Category updated successfully',
            'notification_category': {
                'id': notification_category.id,
                'name': notification_category.name,
                'code': notification_category.code,
                'description': notification_category.description,
                'is_active': notification_category.is_active,
                'edit_url': reverse('notification_category_update', args=[notification_category.id]),
                'delete_url': reverse('notification_category_delete', args=[notification_category.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    notification_category = get_object_or_404(NotificationCategory, pk=pk)
    notification_category.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Notification Category deleted successfully'})
    
    messages.success(request, 'Notification Category deleted successfully')
    return redirect('notification_category_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = NotificationCategory.objects.all()

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
