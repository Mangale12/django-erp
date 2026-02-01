from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import NotificationTemplate


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "channel", "label": "Channel", "type": "text", "required": True},
        {"name": "template_category", "label": "Template Category", "type": "text", "required": True},
        {"name": "template_content", "label": "Template Content", "type": "text", "required": True},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/notification_template.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                notification_template = NotificationTemplate.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    channel=request.POST.get('channel'),
                    template_category=request.POST.get('template_category'),
                    template_content=request.POST.get('template_content'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Notification Template created successfully',
                        'notification_template': {
                            'id': notification_template.id,
                            'name': notification_template.name,
                            'code': notification_template.code,
                            'channel': notification_template.channel,
                            'template_category': notification_template.template_category,
                            'template_content': notification_template.template_content,
                            'is_active': notification_template.is_active,
                            'edit_url': reverse('notification_template_update', args=[notification_template.id]),
                            'delete_url': reverse('notification_template_delete', args=[notification_template.id]),
                        }
                    })
                
                messages.success(request, 'Notification Template created successfully')
                return redirect('notification_template_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating notification template: {str(e)}')
            return redirect('notification_template_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/notification_template/form.html')


def edit(request, pk):
    """Return room view type data as JSON"""
    notification_template = get_object_or_404(NotificationTemplate, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': notification_template.id,
            'name': notification_template.name,
            'code': notification_template.code,
            'channel': notification_template.channel,
            'template_category': notification_template.template_category,
            'template_content': notification_template.template_content,
            'is_active': notification_template.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for account types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    notification_template = get_object_or_404(NotificationTemplate, pk=pk)
    
    try:
        notification_template.name = request.POST.get('name')
        notification_template.code = request.POST.get('code')
        notification_template.channel = request.POST.get('channel')
        notification_template.template_category = request.POST.get('template_category')
        notification_template.template_content = request.POST.get('template_content')
        notification_template.is_active = bool(request.POST.get('is_active'))
        notification_template.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Notification Template updated successfully',
            'notification_template': {
                'id': notification_template.id,
                'name': notification_template.name,
                'code': notification_template.code,
                'channel': notification_template.channel,
                'template_category': notification_template.template_category,
                'template_content': notification_template.template_content,
                'is_active': notification_template.is_active,
                'edit_url': reverse('notification_template_update', args=[notification_template.id]),
                'delete_url': reverse('notification_template_delete', args=[notification_template.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    notification_template = get_object_or_404(NotificationTemplate, pk=pk)
    notification_template.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Notification Template deleted successfully'})
    
    messages.success(request, 'Notification Template deleted successfully')
    return redirect('notification_template_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = NotificationTemplate.objects.all()

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