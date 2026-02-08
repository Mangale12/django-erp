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
        {"name": "food_type", "label": "Food Type", "type": "select_static", "required": True, "values": MenuItem.FOOD_TYPE },
        {"name": "recipe_linked", "label": "Recipe Linked", "type": "checkbox", "default": True},
        {"name": "printer", "label": "Printer", "type": "select", "required": True, "url": reverse('printer_select')}
    ]
    return render(request, 'restaurant_menu/menu_item/list.html', {
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        try:
            with transaction.atomic():
                # ✅ Get the MenuCategory instance
                menu_category_id = request.POST.get('menu_category')
                menu_category = get_object_or_404(MenuCategory, id=menu_category_id)
                # ✅ Get the MenuSubCategory instance
                menu_sub_category_id = request.POST.get('menu_sub_category')
                menu_sub_category = get_object_or_404(MenuSubCategory, id=menu_sub_category_id)
                # ✅ Get the TaxType instance
                tax_type_id = request.POST.get('tax_type')
                tax_type = get_object_or_404(TaxType, id=tax_type_id)
                # ✅ Get the Printer instance
                printer_id = request.POST.get('printer')
                printer = get_object_or_404(Printer, id=printer_id)
                menu_item = MenuItem.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    price=request.POST.get('price'),
                    menu_category=menu_category,  # ← Now it's a proper instance
                    menu_sub_category=menu_sub_category,
                    tax_type=tax_type,
                    food_type=request.POST.get('food_type'),
                    recipe_linked=bool(request.POST.get('recipe_linked')),
                    printer=printer,
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Menu Item created successfully',
                        'menu_item': {
                            'id': menu_item.id,
                            'name': menu_item.name,
                            'description': menu_item.description,
                            'price': str(menu_item.price),  # Decimal → string
                            'menu_category': menu_item.menu_category.id,  # or .name if you prefer
                            'menu_sub_category': menu_item.menu_sub_category.id,
                            'tax_type': menu_item.tax_type.id,
                            'food_type': menu_item.food_type,
                            'recipe_linked': menu_item.recipe_linked,
                            'printer': menu_item.printer.id,
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


def update(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    menu_category = get_object_or_404(MenuCategory, id=menu_item.menu_category_id)
    menu_sub_category = get_object_or_404(MenuSubCategory, id=menu_item.menu_sub_category_id)
    tax_type = get_object_or_404(TaxType, id=menu_item.tax_type_id)
    printer = get_object_or_404(Printer, id=menu_item.printer_id)
    if request.method == 'POST':
        menu_item.name = request.POST.get('name')
        menu_item.description = request.POST.get('description')
        menu_item.is_active = True if request.POST.get('is_active') else False
        menu_item.menu_category = get_object_or_404(MenuCategory, id=request.POST.get('menu_category'))
        menu_item.menu_sub_category = get_object_or_404(MenuSubCategory, id=request.POST.get('menu_sub_category'))
        menu_item.tax_type = get_object_or_404(TaxType, id=request.POST.get('tax_type'))
        menu_item.food_type = request.POST.get('food_type')
        menu_item.recipe_linked = True if request.POST.get('recipe_linked') else False
        menu_item.printer = get_object_or_404(Printer, id=request.POST.get('printer'))
        menu_item.save()

        messages.success(request, 'Menu Item updated successfully')
        return redirect('menu_item_list')

    return render(request, 'restaurant_menu/menu_item/form.html', {
        'menu_item': menu_item,
        'menu_category': menu_category,
        'menu_sub_category': menu_sub_category,
        'tax_type': tax_type,
        'printer': printer
    })


def edit(request, pk):
    """Return menu item data as JSON"""
    menu_item = get_object_or_404(MenuItem, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': menu_item.id,
            'name': menu_item.name,
            'description': menu_item.description,
            'is_active': menu_item.is_active,
        }
    }
    return JsonResponse(data)


def update_ajax(request, pk):
    """Handle AJAX updates for menu items"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    menu_item = get_object_or_404(MenuItem, pk=pk)
    
    try:
        menu_item.name = request.POST.get('name')
        menu_item.description = request.POST.get('description', '')
        menu_item.is_active = bool(request.POST.get('is_active'))
        menu_item.menu_category_id = request.POST.get('menu_category')
        menu_item.menu_sub_category_id = request.POST.get('menu_sub_category')
        menu_item.tax_type_id = request.POST.get('tax_type')
        menu_item.food_type = request.POST.get('food_type')
        menu_item.recipe_linked = True if request.POST.get('recipe_linked') else False
        menu_item.printer_id = request.POST.get('printer')
        menu_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Menu Item updated successfully',
            'menu_item': {
                'id': menu_item.id,
                'name': menu_item.name,
                'description': menu_item.description,
                'is_active': menu_item.is_active,
                'edit_url': reverse('menu_item_update', args=[menu_item.id]),
                'delete_url': reverse('menu_item_delete', args=[menu_item.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    menu_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Menu Item deleted successfully'})
    
    messages.success(request, 'Menu Item deleted successfully')
    return redirect('menu_item_list')

def show(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    return render(request, 'restaurant_menu/menu_item/show.html', {
        'menu_item': menu_item
    })

def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = MenuItem.objects.all()

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
    