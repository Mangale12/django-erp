from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.forms.models import model_to_dict
from hotel_app.restaurant_menu.models import MenuSubCategory, MenuCategory


def index(request):
    menu_sub_categories = MenuSubCategory.objects.all()
    fields = [
        {"name": "name", "label": "Name", "type": "text", "required": True},
        {"name": "code", "label": "Code", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "menu_category", "label": "Menu Category", "type": "select", "required": True, 'url': reverse('menu_category_select')},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True}
    ]
    return render(request, 'restaurant_menu/menu_sub_category/list.html', {
        'menu_sub_categories': menu_sub_categories,
        'fields': fields
    })


@require_http_methods(["GET", "POST"])
def create(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        try:
            with transaction.atomic():
                menu_category_id = request.POST.get('menu_category')
                menu_category = get_object_or_404(MenuCategory, id=menu_category_id)

                menu_sub_category = MenuSubCategory.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    description=request.POST.get('description'),
                    menu_category=menu_category,  # ✅ FK object, safer
                    is_active=request.POST.get('is_active') == 'on',
                )

                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Menu Sub Category created successfully',
                        'menu_sub_category': {
                            'id': menu_sub_category.id,
                            'name': menu_sub_category.name,
                            'code': menu_sub_category.code,
                            'description': menu_sub_category.description,
                            'menu_category': {
                                'id': menu_category.id,
                                'name': menu_category.name,
                            },
                            'is_active': menu_sub_category.is_active,
                            'edit_url': reverse('menu_sub_category_update', args=[menu_sub_category.id]),
                            'delete_url': reverse('menu_sub_category_delete', args=[menu_sub_category.id]),
                        }
                    })

                messages.success(request, 'Menu Sub Category created successfully')
                return redirect('menu_sub_category_list')

        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)

            messages.error(request, f'Error creating menu sub category: {e}')
            return redirect('menu_sub_category_list')

    # GET request
    return render(request, 'restaurant_menu/menu_sub_category/form.html')

def update(request, pk):
    menu_sub_category = get_object_or_404(MenuSubCategory, pk=pk)
    if request.method == 'POST':
        menu_sub_category.name = request.POST.get('name')
        menu_sub_category.code = request.POST.get('code')
        menu_sub_category.description = request.POST.get('description')
        menu_sub_category.menu_category_id = request.POST.get('menu_category')
        menu_sub_category.is_active = True if request.POST.get('is_active') else False
        menu_sub_category.save()

        messages.success(request, 'Menu Sub Category updated successfully')
        return redirect('menu_sub_category_list')
    
    return render(request, 'restaurant_menu/menu_sub_category/form.html', {
        'menu_sub_category': menu_sub_category
    })


def edit(request, pk):
    """Return menu sub category data as JSON"""
    menu_sub_category = get_object_or_404(MenuSubCategory, pk=pk)
    data = {
        'success': True,
        'data': {
            'id': menu_sub_category.id,
            'name': menu_sub_category.name,
            'code': menu_sub_category.code,
            'description': menu_sub_category.description,
            'menu_category': menu_sub_category.menu_category,
            'is_active': menu_sub_category.is_active,
        }
    }
    return JsonResponse(data)


def update_ajax(request, pk):
    """Handle AJAX updates for menu sub categories"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    menu_sub_category = get_object_or_404(MenuSubCategory, pk=pk)
    
    try:
        menu_sub_category.name = request.POST.get('name')
        menu_sub_category.code = request.POST.get('code')
        menu_sub_category.description = request.POST.get('description', '')
        menu_sub_category.is_active = bool(request.POST.get('is_active'))
        menu_sub_category.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Menu Sub Category updated successfully',
            'menu_sub_category': {
                'id': menu_sub_category.id,
                'name': menu_sub_category.name,
                'code': menu_sub_category.code,
                'description': menu_sub_category.description,
                'menu_category': menu_sub_category.menu_category,
                'is_active': menu_sub_category.is_active,
                'edit_url': reverse('menu_sub_category_update', args=[menu_sub_category.id]),
                'delete_url': reverse('menu_sub_category_delete', args=[menu_sub_category.id]),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def delete(request, pk):
    menu_sub_category = get_object_or_404(MenuSubCategory, pk=pk)
    menu_sub_category.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Menu Sub Category deleted successfully'})
    
    messages.success(request, 'Menu Sub Category deleted successfully')
    return redirect('menu_sub_category_list')


def menu_sub_categories(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = MenuSubCategory.objects.all()

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


def select(request):
    return JsonResponse({
        "results": results
    })
