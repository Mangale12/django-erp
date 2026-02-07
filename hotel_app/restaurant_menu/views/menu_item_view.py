from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from hotel_app.restaurant_menu.models import MenuItem, MenuCategory


def index(request):
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "menu_category", "label": "Menu Category", "type": "select", "required": True, "url": reverse('menu_category_select')},
        {"name": "menu_sub_category", "label": "Menu Sub Category", "type": "select", "required": True, "url": reverse('menu_sub_category_select')},
        {"name": "price", "label": "Price", "type": "number", "required": True},
        {"name": "description", "label": "Description", "type": "textarea", "required": True},
        {"name": "tax_type", "label": "Tax Type", "type": "select", "required": True, "url": reverse('tax_type_select')},
        {"name": "food_type", "label": "Food Type", "type": "select_static", "required": True, "values": MenuItem.FOOT_TYPE},
        {"name": "recipe_linked", "label": "Recipe Linked", "type": "checkbox", "default": True},
        {"name": "printer", "label": "Printer", "type": "select", "required": True, "url": reverse('printer_select')}
    ]
    return render(request, 'restaurant_menu/menu_item/list.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def menu_item_create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        try:
            with transaction.atomic():
                # ✅ Get the MenuCategory instance
                menu_category_id = request.POST.get('menu_category')
                menu_category = get_object_or_404(MenuCategory, id=menu_category_id)

                menu_item = MenuItem.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    price=request.POST.get('price'),
                    menu_category=menu_category,  # ← Now it's a proper instance
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Menu Item created successfully',
                        'menu_item': {
                            'id': menu_item.id,
                            'name': menu_item.name,
                            'code': menu_item.code,
                            'description': menu_item.description,
                            'price': str(menu_item.price),  # Decimal → string
                            'menu_category': menu_item.menu_category.id,  # or .name if you prefer
                            'is_active': menu_item.is_active,
                        }
                    })
                
                messages.success(request, 'Menu Item created successfully')
                return redirect('menu_item_list')
                
        except MenuCategory.DoesNotExist:
            error_msg = "Selected menu category does not exist."
            if is_ajax:
                return JsonResponse({'success': False, 'error': error_msg}, status=400)
            messages.error(request, error_msg)
            return redirect('menu_item_list')
            
        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            messages.error(request, f'Error creating menu item: {str(e)}')
            return redirect('menu_item_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'restaurant_menu/menu_item/form.html')


def menu_item_update(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)

    if request.method == 'POST':
        menu_item.name = request.POST.get('name')
        menu_item.code = request.POST.get('code')
        menu_item.description = request.POST.get('description')
        menu_item.is_active = True if request.POST.get('is_active') else False
        menu_item.save()

        messages.success(request, 'Menu Item updated successfully')
        return redirect('menu_item_list')

    return render(request, 'restaurant_menu/menu_item/form.html', {
        'menu_item': menu_item
    })


def menu_item_edit(request, pk):
    """Return menu item data as JSON"""
    menu_item = get_object_or_404(MenuItem, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': menu_item.id,
            'name': menu_item.name,
            'code': menu_item.code,
            'description': menu_item.description,
            'is_active': menu_item.is_active,
        }
    }
    return JsonResponse(data)


def menu_item_update_ajax(request, pk):
    """Handle AJAX updates for menu items"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    menu_item = get_object_or_404(MenuItem, pk=pk)
    
    try:
        menu_item.name = request.POST.get('name')
        menu_item.code = request.POST.get('code')
        menu_item.description = request.POST.get('description', '')
        menu_item.is_active = bool(request.POST.get('is_active'))
        menu_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Menu Item updated successfully',
            'menu_item': {
                'id': menu_item.id,
                'name': menu_item.name,
                'code': menu_item.code,
                'description': menu_item.description,
                'is_active': menu_item.is_active,
                'edit_url': reverse('menu_item_update', args=[menu_item.id]),
                'delete_url': reverse('menu_item_delete', args=[menu_item.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def menu_item_delete(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    menu_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Menu Item deleted successfully'})
    
    messages.success(request, 'Menu Item deleted successfully')
    return redirect('menu_item_list')
