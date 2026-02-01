from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from restaurant_menu.models import MenuCategory


def menu_category_list(request):
    menu_categories = MenuCategory.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'restaurant_menu/menu_category/list.html', {
        'menu_categories': menu_categories,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def menu_category_create(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():
                menu_category = MenuCategory.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    is_active=bool(request.POST.get('is_active')),
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Menu Category created successfully',
                        'menu_category': {
                            'id': menu_category.id,
                            'name': menu_category.name,
                            'code': menu_category.code,
                            'description': menu_category.description,
                            'is_active': menu_category.is_active,
                            'edit_url': reverse('menu_category_update', args=[menu_category.id]),
                            'delete_url': reverse('menu_category_delete', args=[menu_category.id]),
                        }
                    })
                
                messages.success(request, 'Menu Category created successfully')
                return redirect('menu_category_list')
                
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error creating menu category: {str(e)}')
            return redirect('menu_category_list')

    # GET request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    return render(request, 'restaurant_menu/menu_category/form.html')


def menu_category_update(request, pk):
    food_type = get_object_or_404(FoodType, pk=pk)

    if request.method == 'POST':
        food_type.name = request.POST.get('name')
        food_type.code = request.POST.get('code')
        food_type.description = request.POST.get('description')
        food_type.is_active = True if request.POST.get('is_active') else False
        food_type.save()

        messages.success(request, 'Menu Category updated successfully')
        return redirect('menu_category_list')

    return render(request, 'restaurant_menu/menu_category/form.html', {
        'menu_category': menu_category
    })


def menu_category_edit(request, pk):
    """Return menu category data as JSON"""
    menu_category = get_object_or_404(MenuCategory, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': menu_category.id,
            'name': menu_category.name,
            'code': menu_category.code,
            'description': menu_category.description,
            'is_active': menu_category.is_active,
        }
    }
    return JsonResponse(data)


def menu_category_update_ajax(request, pk):
    """Handle AJAX updates for menu categories"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    menu_category = get_object_or_404(MenuCategory, pk=pk)
    
    try:
        menu_category.name = request.POST.get('name')
        menu_category.code = request.POST.get('code')
        menu_category.description = request.POST.get('description', '')
        menu_category.is_active = bool(request.POST.get('is_active'))
        menu_category.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Menu Category updated successfully',
            'menu_category': {
                'id': menu_category.id,
                'name': menu_category.name,
                'code': menu_category.code,
                'description': menu_category.description,
                'is_active': menu_category.is_active,
                'edit_url': reverse('menu_category_update', args=[menu_category.id]),
                'delete_url': reverse('menu_category_delete', args=[menu_category.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def menu_category_delete(request, pk):
    menu_category = get_object_or_404(MenuCategory, pk=pk)
    menu_category.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Menu Category deleted successfully'})
    
    messages.success(request, 'Menu Category deleted successfully')
    return redirect('menu_category_list')


def menu_categories(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = MenuCategory.objects.all()

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
