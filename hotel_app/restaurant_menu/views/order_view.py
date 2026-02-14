from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from hotel_app.restaurant_menu.models import MenuItem, MenuCategory, MenuSubCategory, Order, OrderItem, OrderItemModifier


def index(request):
    fields = [
        {"name": "table", "label": "Table", "type": "select", "required": True, "url": reverse('table_setup_select')},
        {"name": "guest_count", "label": "Guest Count", "type": "number", "required": True},
        {"name": "guest_name", "label": "Guest Name", "type": "text", "required": False},
        {"name": "room", "label": "Room", "type": "select", "required": False, "url": reverse('room_select')},
        {"name": "order_start_time", "label": "Order Start Time", "type": "datetime", "required": True},
        {"name": "order_status", "label": "Order Status", "type": "select_static", "required": True, "values": Order.ORDER_STATUS },
        {"name" : "menu_items", "label": "Menu Items", "type": "select", "required": True, "url": reverse('menu_item_select')},
        {"name" : "quantity", "label": "Quantity", "type": "number", "required": True},
        {"name" : "unit_price", "label": "Unit Price", "type": "number", "required": True},
        {"name" : "total_price", "label": "Total Price", "type": "number", "required": True},
        {"name" : "order_item_status", "label": "Order Item Status", "type": "select_static", "required": True, "values": OrderItem.ORDER_ITEM_STATUS },
        {"name" : "modifiers", "label": "Modifiers", "type": "select", "required": True, "url": reverse('modifier_select')},
        {"name" : "cancel_reason", "label": "Cancel Reason", "type": "text", "required": False}
    ]
    return render(request, 'restaurant_menu/order/list.html', {
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
                order = Order.objects.create(
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
                        'message': 'Order created successfully',
                        'order': {
                            'id': order.id,
                            'name': order.name,
                            'description': order.description,
                            'price': str(order.price),  # Decimal → string
                            'menu_category': order.menu_category.id,  # or .name if you prefer
                            'menu_sub_category': order.menu_sub_category.id,
                            'tax_type': order.tax_type.id,
                            'food_type': order.food_type,
                            'recipe_linked': order.recipe_linked,
                            'printer': order.printer.id,
                            'is_active': order.is_active,
                        }
                    })
                
                messages.success(request, 'Order created successfully')
                return redirect('order_list')
                
        except MenuCategory.DoesNotExist:
            error_msg = "Selected menu category does not exist."
            if is_ajax:
                return JsonResponse({'success': False, 'error': error_msg}, status=400)
            messages.error(request, error_msg)
            return redirect('order_list')
            
        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            messages.error(request, f'Error creating order: {str(e)}')
            return redirect('order_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'restaurant_menu/order/form.html')


def update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    menu_category = get_object_or_404(MenuCategory, id=order.menu_category_id)
    menu_sub_category = get_object_or_404(MenuSubCategory, id=order.menu_sub_category_id)
    tax_type = get_object_or_404(TaxType, id=order.tax_type_id)
    printer = get_object_or_404(Printer, id=order.printer_id)
    if request.method == 'POST':
        order.name = request.POST.get('name')
        order.description = request.POST.get('description')
        order.is_active = True if request.POST.get('is_active') else False
        order.menu_category = get_object_or_404(MenuCategory, id=request.POST.get('menu_category'))
        order.menu_sub_category = get_object_or_404(MenuSubCategory, id=request.POST.get('menu_sub_category'))
        order.tax_type = get_object_or_404(TaxType, id=request.POST.get('tax_type'))
        order.food_type = request.POST.get('food_type')
        order.recipe_linked = True if request.POST.get('recipe_linked') else False
        order.printer = get_object_or_404(Printer, id=request.POST.get('printer'))
        order.save()

        messages.success(request, 'Order updated successfully')
        return redirect('order_list')

    return render(request, 'restaurant_menu/order/form.html', {
        'order': order,
        'menu_category': menu_category,
        'menu_sub_category': menu_sub_category,
        'tax_type': tax_type,
        'printer': printer
    })


def edit(request, pk):
    """Return menu item data as JSON"""
    order = get_object_or_404(Order, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': order.id,
            'name': order.name,
            'description': order.description,
            'is_active': order.is_active,
        }
    }
    return JsonResponse(data)


def update_ajax(request, pk):
    """Handle AJAX updates for menu items"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    order = get_object_or_404(Order, pk=pk)
    
    try:
        order.name = request.POST.get('name')
        order.description = request.POST.get('description', '')
        order.is_active = bool(request.POST.get('is_active'))
        order.menu_category_id = request.POST.get('menu_category')
        order.menu_sub_category_id = request.POST.get('menu_sub_category')
        order.tax_type_id = request.POST.get('tax_type')
        order.food_type = request.POST.get('food_type')
        order.recipe_linked = True if request.POST.get('recipe_linked') else False
        order.printer_id = request.POST.get('printer')
        order.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Order updated successfully',
            'order': {
                'id': order.id,
                'name': order.name,
                'description': order.description,
                'is_active': order.is_active,
                'edit_url': reverse('order_update', args=[order.id]),
                'delete_url': reverse('order_delete', args=[order.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Order deleted successfully'})
    
    messages.success(request, 'Order deleted successfully')
    return redirect('order_list')

def show(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'restaurant_menu/order/show.html', {
        'order': order
    })

def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = Order.objects.all()

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
    