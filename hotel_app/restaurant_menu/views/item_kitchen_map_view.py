from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from hotel_app.restaurant_menu.models import Kitchen, KitchenStation, MenuItem, ItemKitchenMap  # your models

from django.contrib.auth.decorators import login_required


def index(request):
    """
    Render the main Kitchen list page
    """

    fields = [
        {"name": "menu_item", "label": "Menu Item", "type": "select", "url": reverse('menu_item_select'), "required": True},
        {"name": "kitchen", "label": "Kitchen", "type": "select", "url": reverse('kitchen_select'), "required": True},
        {"name": "kitchen_station", "label": "Kitchen Station", "type": "select", "url": reverse('kitchen_station_select'), "required": True},
        {"name": "expected_time", "label": "Expected Time", "type": "number", "required": True},
    ]

    return render(request, 'restaurant_menu/item_kitchen_map/list.html', {
        'fields': fields
    })

@login_required
@require_http_methods(["GET", "POST"])

def create(request):
    """
    Create Kitchen (normal POST or AJAX)
    """
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        try:
            with transaction.atomic():
                item_kitchen_map = ItemKitchenMap.objects.create(
                    menu_item=get_object_or_404(MenuItem, pk=request.POST.get('menu_item')),
                    kitchen=get_object_or_404(Kitchen, pk=request.POST.get('kitchen')),
                    kitchen_station=get_object_or_404(KitchenStation, pk=request.POST.get('kitchen_station')),
                    expected_time=request.POST.get('expected_time'),
                )

                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Item Kitchen Map created successfully',
                        'item_kitchen_map': {
                            'id': item_kitchen_map.id,
                            'menu_item': item_kitchen_map.menu_item.id,
                            'kitchen': item_kitchen_map.kitchen.id,
                            'kitchen_station': item_kitchen_map.kitchen_station.id,
                            'expected_time': item_kitchen_map.expected_time,
                            'edit_url': reverse('item_kitchen_map_update', args=[item_kitchen_map.id]),
                            'delete_url': reverse('item_kitchen_map_delete', args=[item_kitchen_map.id]),
                        }
                    })

                messages.success(request, 'Item Kitchen Map created successfully')
                return redirect('item_kitchen_map_list')

        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            messages.error(request, f'Error creating item kitchen map: {str(e)}')
            return redirect('item_kitchen_map_list')

    return render(request, 'restaurant_menu/item_kitchen_map/form.html')


def edit(request, pk):
    """
    Return item kitchen map data for AJAX edit
    """
    item_kitchen_map = get_object_or_404(ItemKitchenMap, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': item_kitchen_map.id,
            'menu_item': item_kitchen_map.menu_item.id,
            'kitchen': item_kitchen_map.kitchen.id,
            'kitchen_station': item_kitchen_map.kitchen_station.id,
            'expected_time': item_kitchen_map.expected_time,
        }
    }
    return JsonResponse(data)


@require_http_methods(["POST"])
def update(request, pk):
    """
    Update Item Kitchen Map via AJAX
    """
    item_kitchen_map = get_object_or_404(ItemKitchenMap, pk=pk)

    try:
        item_kitchen_map.menu_item = get_object_or_404(MenuItem, pk=request.POST.get('menu_item'))
        item_kitchen_map.kitchen = get_object_or_404(Kitchen, pk=request.POST.get('kitchen'))
        item_kitchen_map.kitchen_station = get_object_or_404(KitchenStation, pk=request.POST.get('kitchen_station'))
        item_kitchen_map.expected_time = request.POST.get('expected_time')
        item_kitchen_map.save()

        return JsonResponse({
            'success': True,
            'message': 'Item Kitchen Map updated successfully',
            'item_kitchen_map': {
                'id': item_kitchen_map.id,
                'menu_item': item_kitchen_map.menu_item.id,
                'kitchen': item_kitchen_map.kitchen.id,
                'kitchen_station': item_kitchen_map.kitchen_station.id,
                'expected_time': item_kitchen_map.expected_time,
                'edit_url': reverse('item_kitchen_map_update', args=[item_kitchen_map.id]),
                'delete_url': reverse('item_kitchen_map_delete', args=[item_kitchen_map.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    """
    Delete Item Kitchen Map (normal or AJAX)
    """
    item_kitchen_map = get_object_or_404(ItemKitchenMap, pk=pk)
    item_kitchen_map.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Item Kitchen Map deleted successfully'})

    messages.success(request, 'Item Kitchen Map deleted successfully')
    return redirect('item_kitchen_map_list')


def select(request):
    """
    Select2 AJAX endpoint
    """
    keyword = request.GET.get('term', '').strip()
    qs = ItemKitchenMap.objects.all()
    if keyword:
        qs = qs.filter(name__icontains=keyword)

    qs = qs.order_by('-created_at')[:5]

    results = [{"id": k.id, "text": k.name} for k in qs]
    return JsonResponse({"results": results})
