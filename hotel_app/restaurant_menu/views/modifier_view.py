from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from hotel_app.restaurant_menu.models import Modifier, MenuItem
from hotel_app.restaurant_menu.forms import ModifierForm
from hotel_app.restaurant_menu.views.menu_item_view import select as menu_item_select


def index(request):
    modifiers = Modifier.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "extra_price", "label": "Extra Price", "type": "number", "required": True},
        {"name": "menu_item", "label": "Menu Item", "type": "select", "required": True, 'url': reverse('menu_item_select')},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'restaurant_menu/modifier/list.html', {
        'modifiers': modifiers,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        try:
            with transaction.atomic():
                menu_item = get_object_or_404(MenuItem, id=request.POST.get('menu_item'))
                modifier = Modifier.objects.create(
                    name=request.POST.get('name'),
                    description=request.POST.get('description'),
                    extra_price=request.POST.get('extra_price'),
                    menu_item=menu_item,
                    is_active=request.POST.get('is_active') == 'on',
                )

                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Modifier created successfully',
                        'modifier': {
                            'id': modifier.id,
                            'name': modifier.name,
                            'description': modifier.description,
                            'extra_price': modifier.extra_price,
                            'menu_item': modifier.menu_item.id,
                            'is_active': modifier.is_active,
                            'edit_url': reverse('modifier_update', args=[modifier.id]),
                            'delete_url': reverse('modifier_delete', args=[modifier.id]),
                        }
                    })

                messages.success(request, 'Modifier created successfully')
                return redirect('modifier_list')

        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)

            messages.error(request, f'Error creating modifier: {e}')
            return redirect('modifier_list')

    # GET request
    return render(request, 'restaurant_menu/modifier/form.html')


def update(request, pk):
    modifier = get_object_or_404(Modifier, pk=pk)
    if request.method == 'POST':
        modifier.name = request.POST.get('name')
        modifier.description = request.POST.get('description')
        modifier.extra_price = request.POST.get('extra_price')
        modifier.menu_item_id = get_object_or_404(MenuItem, id=request.POST.get('menu_item'))
        modifier.is_active = True if request.POST.get('is_active') else False
        modifier.save()

        messages.success(request, 'Modifier updated successfully')
        return redirect('modifier_list')
    
    return render(request, 'restaurant_menu/modifier/form.html', {
        'modifier': modifier
    })


def edit(request, pk):
    """Return modifier data as JSON"""
    modifier = get_object_or_404(Modifier, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': modifier.id,
            'name': modifier.name,
            'description': modifier.description,
            'extra_price': modifier.extra_price,
            'menu_item': modifier.menu_item.id,
            'is_active': modifier.is_active,
        }
    }
    return JsonResponse(data)


def update_ajax(request, pk):
    """Handle AJAX updates for modifiers"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    modifier = get_object_or_404(Modifier, pk=pk)
    
    try:
        modifier.name = request.POST.get('name')
        modifier.description = request.POST.get('description', '')
        modifier.extra_price = request.POST.get('extra_price')
        modifier.menu_item_id = get_object_or_404(MenuItem, id=request.POST.get('menu_item'))
        modifier.is_active = bool(request.POST.get('is_active'))
        modifier.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Modifier updated successfully',
            'modifier': {
                'id': modifier.id,
                'name': modifier.name,
                'description': modifier.description,
                'extra_price': modifier.extra_price,
                'menu_item': modifier.menu_item.id,
                'is_active': modifier.is_active,
                'edit_url': reverse('modifier_update', args=[modifier.id]),
                'delete_url': reverse('modifier_delete', args=[modifier.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    modifier = get_object_or_404(Modifier, pk=pk)
    modifier.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Modifier deleted successfully'})
    
    messages.success(request, 'Modifier deleted successfully')
    return redirect('modifier_list')


def show(request, pk):
    modifier = get_object_or_404(Modifier, pk=pk)
    return render(request, 'restaurant_menu/modifier/show.html', {
        'modifier': modifier
    })


def select(request):
    keyword = (request.GET.get('term') or request.GET.get('q') or '').strip()

    qs = Modifier.objects.all()

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
        "results": results,
        "pagination": {
            "more": False
        }
    })

    
