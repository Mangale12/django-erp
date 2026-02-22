from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from hotel_app.restaurant_menu.models import Property, PropertySettings


def _build_fields():
    return [
        {
            "name": "property",
            "label": "Property",
            "type": "select",
            "url": reverse("property_select"),
            "required": True,
        },
        {"name": "enable_kot_module", "label": "Enable KOT Module", "type": "checkbox"},
        {"name": "enable_table_management", "label": "Enable Table Management", "type": "checkbox"},
        {"name": "enable_room_module", "label": "Enable Room Module", "type": "checkbox"},
        {"name": "enable_folio_module", "label": "Enable Folio Module", "type": "checkbox"},
        {"name": "enable_laundry_module", "label": "Enable Laundry Module", "type": "checkbox"},
        {"name": "enable_spa_module", "label": "Enable Spa Module", "type": "checkbox"},
        {"name": "enable_inventory_module", "label": "Enable Inventory Module", "type": "checkbox"},
        {"name": "enable_credit_sales", "label": "Enable Credit Sales", "type": "checkbox"},
        {"name": "enable_multi_outlet", "label": "Enable Multi Outlet", "type": "checkbox"},
    ]


def _save_property_settings_from_post(settings_obj, post_data):
    property_id = post_data.get("property")
    if not property_id:
        raise ValueError("Property is required.")

    property_obj = get_object_or_404(Property, pk=property_id)

    duplicate = PropertySettings.objects.filter(property=property_obj).exclude(pk=settings_obj.pk).exists()
    if duplicate:
        raise ValueError("Settings for the selected property already exist.")

    settings_obj.property = property_obj
    settings_obj.enable_kot_module = bool(post_data.get("enable_kot_module"))
    settings_obj.enable_table_management = bool(post_data.get("enable_table_management"))
    settings_obj.enable_room_module = bool(post_data.get("enable_room_module"))
    settings_obj.enable_folio_module = bool(post_data.get("enable_folio_module"))
    settings_obj.enable_laundry_module = bool(post_data.get("enable_laundry_module"))
    settings_obj.enable_spa_module = bool(post_data.get("enable_spa_module"))
    settings_obj.enable_inventory_module = bool(post_data.get("enable_inventory_module"))
    settings_obj.enable_credit_sales = bool(post_data.get("enable_credit_sales"))
    settings_obj.enable_multi_outlet = bool(post_data.get("enable_multi_outlet"))

    settings_obj.save()
    return settings_obj


@login_required
def index(request):
    return render(
        request,
        "restaurant_menu/property_settings/list.html",
        {"fields": _build_fields()},
    )


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "GET":
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Invalid request method"}, status=405)
        return redirect("property_settings_list")

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    try:
        with transaction.atomic():
            _save_property_settings_from_post(PropertySettings(), request.POST)
        if is_ajax:
            return JsonResponse({"success": True, "message": "Property settings created successfully"})
        messages.success(request, "Property settings created successfully")
        return redirect("property_settings_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error creating property settings: {exc}")
        return redirect("property_settings_list")


@login_required
@require_http_methods(["POST"])
def update(request, pk):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    settings_obj = get_object_or_404(PropertySettings, pk=pk)
    try:
        with transaction.atomic():
            _save_property_settings_from_post(settings_obj, request.POST)
        if is_ajax:
            return JsonResponse({"success": True, "message": "Property settings updated successfully"})
        messages.success(request, "Property settings updated successfully")
        return redirect("property_settings_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error updating property settings: {exc}")
        return redirect("property_settings_list")


@login_required
def edit(request, pk):
    settings_obj = get_object_or_404(PropertySettings, pk=pk)
    payload = {
        "id": settings_obj.pk,
        "property": settings_obj.property_id,
        "enable_kot_module": settings_obj.enable_kot_module,
        "enable_table_management": settings_obj.enable_table_management,
        "enable_room_module": settings_obj.enable_room_module,
        "enable_folio_module": settings_obj.enable_folio_module,
        "enable_laundry_module": settings_obj.enable_laundry_module,
        "enable_spa_module": settings_obj.enable_spa_module,
        "enable_inventory_module": settings_obj.enable_inventory_module,
        "enable_credit_sales": settings_obj.enable_credit_sales,
        "enable_multi_outlet": settings_obj.enable_multi_outlet,
    }
    return JsonResponse(
        {
            "success": True,
            "data": payload,
            "id": settings_obj.pk,
            "property": settings_obj.property_id,
            "enable_kot_module": settings_obj.enable_kot_module,
            "enable_table_management": settings_obj.enable_table_management,
            "enable_room_module": settings_obj.enable_room_module,
            "enable_folio_module": settings_obj.enable_folio_module,
            "enable_laundry_module": settings_obj.enable_laundry_module,
            "enable_spa_module": settings_obj.enable_spa_module,
            "enable_inventory_module": settings_obj.enable_inventory_module,
            "enable_credit_sales": settings_obj.enable_credit_sales,
            "enable_multi_outlet": settings_obj.enable_multi_outlet,
        }
    )


@login_required
@require_http_methods(["POST"])
def delete(request, pk):
    settings_obj = get_object_or_404(PropertySettings, pk=pk)
    settings_obj.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "Property settings deleted successfully"})

    messages.success(request, "Property settings deleted successfully")
    return redirect("property_settings_list")


@login_required
def select(request):
    keyword = (request.GET.get("term") or request.GET.get("q") or "").strip()

    queryset = PropertySettings.objects.select_related("property").all()

    if keyword:
        queryset = queryset.filter(property__property_name__icontains=keyword)

    queryset = queryset.order_by("-created_at")[:20]
    results = [{"id": item.pk, "text": item.property.property_name} for item in queryset]

    return JsonResponse({"results": results})
