from django.shortcuts import render, redirect, get_object_or_404, reverse,HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import BookingSource


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/booking_source.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                booking_source = BookingSource.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Booking source created successfully',
                        'booking_source': {
                            'id': booking_source.id,
                            'name': booking_source.name,
                            'code': booking_source.code,
                            'description': booking_source.description,
                            'is_active': booking_source.is_active,
                            'edit_url': reverse('booking_source_update', args=[booking_source.id]),
                            'delete_url': reverse('booking_source_delete', args=[booking_source.id]),
                        }
                    })
                
                messages.success(request, 'Booking source created successfully')
                return redirect('booking_source_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating booking source: {str(e)}')
            return redirect('booking_source_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/currency/form.html')



def edit(request, pk):
    """Return room view type data as JSON"""
    booking_source = get_object_or_404(BookingSource, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': booking_source.id,
            'name': booking_source.name,
            'code': booking_source.code,
            'description': booking_source.description,
            'is_active': booking_source.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for account types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    booking_source = get_object_or_404(BookingSource, pk=pk)
    
    try:
        booking_source.name = request.POST.get('name')
        booking_source.code = request.POST.get('code')
        booking_source.description = request.POST.get('description', '')
        booking_source.is_active = bool(request.POST.get('is_active'))
        booking_source.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Booking source updated successfully',
            'booking_source': {
                'id': booking_source.id,
                'name': booking_source.name,
                'code': booking_source.code,
                'description': booking_source.description,
                'is_active': booking_source.is_active,
                'edit_url': reverse('booking_source_update', args=[booking_source.id]),
                'delete_url': reverse('booking_source_delete', args=[booking_source.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    booking_source = get_object_or_404(BookingSource, pk=pk)
    booking_source.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Booking source deleted successfully'})
    
    messages.success(request, 'Booking source deleted successfully')
    return redirect('booking_source_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = BookingSource.objects.all()

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