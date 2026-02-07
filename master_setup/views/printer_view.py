from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from master_setup.models import Printer
from datetime import timedelta

def index(request):
    printers = Printer.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "printer_type", "label": "Printer Type", "type": "text", "required": True},
        {"name": "ip_address", "label": "IP Address", "type": "text", "required": True},
        {"name": "port", "label": "Port", "type": "number", "required": True},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'master_setup/printer.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                printer = Printer.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    printer_type=request.POST.get('printer_type'),
                    ip_address=request.POST.get('ip_address'),
                    port=request.POST.get('port'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Printer created successfully',
                    })
                
                messages.success(request, 'Printer created successfully')
                return redirect('printer_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating printer: {str(e)}')
            return redirect('printer_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'master_setup/shift_type/form.html')



def edit(request, pk):
    """Return room view type data as JSON"""
    printer = get_object_or_404(Printer, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': printer.id,
            'name': printer.name,
            'code': printer.code,
            'printer_type': printer.printer_type,
            'ip_address': printer.ip_address,
            'port': printer.port,
            'is_active': printer.is_active,
        }
    }
    return JsonResponse(data)


def update(request, pk):
    """Handle AJAX updates for account types"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    printer = get_object_or_404(Printer, pk=pk)
    
    try:
        printer.name = request.POST.get('name')
        printer.code = request.POST.get('code')
        printer.printer_type = request.POST.get('printer_type')
        printer.ip_address = request.POST.get('ip_address')
        printer.port = request.POST.get('port')
        printer.is_active = bool(request.POST.get('is_active'))
        printer.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Printer updated successfully',
            'printer': {
                'id': printer.id,
                'name': printer.name,
                'code': printer.code,
                'printer_type': printer.printer_type,
                'ip_address': printer.ip_address,
                'port': printer.port,
                'is_active': printer.is_active,
                'edit_url': reverse('printer_update', args=[printer.id]),
                'delete_url': reverse('printer_delete', args=[printer.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    printer = get_object_or_404(Printer, pk=pk)
    printer.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Printer deleted successfully'})
    
    messages.success(request, 'Printer deleted successfully')
    return redirect('printer_list')


def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = Printer.objects.all()

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