from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from hotel_app.restaurant_menu.models import Property


def _build_fields():
    return [
        {"name": "property_code", "label": "Property Code", "type": "text", "required": True},
        {"name": "property_name", "label": "Property Name", "type": "text", "required": True},
        {
            "name": "property_type",
            "label": "Property Type",
            "type": "static_select",
            "required": True,
            "options": Property.PROPERTY_TYPE_CHOICES,
        },
        {"name": "address", "label": "Address", "type": "textarea", "required": True},
        {"name": "city", "label": "City", "type": "text", "required": True},
        {"name": "state", "label": "State", "type": "text", "required": True},
        {"name": "country", "label": "Country", "type": "text", "required": True},
        {"name": "postal_code", "label": "Postal Code", "type": "text"},
        {"name": "phone", "label": "Phone", "type": "text", "required": True},
        {"name": "email", "label": "Email", "type": "email", "required": True},
        {"name": "gst_number", "label": "GST Number", "type": "text"},
        {"name": "currency", "label": "Currency", "type": "text", "required": True, "attributes": {"maxlength": "10"}},
        {"name": "timezone", "label": "Timezone", "type": "text", "required": True, "attributes": {"placeholder": "UTC"}},
        {"name": "website", "label": "Website", "type": "url"},
        {
            "name": "parent_property",
            "label": "Parent Property",
            "type": "select",
            "url": reverse("property_select"),
        },
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True},
    ]


def _save_property_from_post(property_obj, post_data):
    parent_property_id = post_data.get("parent_property")
    parent_property = None
    if parent_property_id:
        parent_property = get_object_or_404(Property, pk=parent_property_id)

    property_obj.property_code = (post_data.get("property_code") or "").strip()
    property_obj.property_name = (post_data.get("property_name") or "").strip()
    property_obj.property_type = post_data.get("property_type") or "RESTAURANT"
    property_obj.address = (post_data.get("address") or "").strip()
    property_obj.city = (post_data.get("city") or "").strip()
    property_obj.state = (post_data.get("state") or "").strip()
    property_obj.country = (post_data.get("country") or "").strip()
    property_obj.postal_code = (post_data.get("postal_code") or "").strip() or None
    property_obj.phone = (post_data.get("phone") or "").strip()
    property_obj.email = (post_data.get("email") or "").strip()
    property_obj.gst_number = (post_data.get("gst_number") or "").strip() or None
    property_obj.currency = (post_data.get("currency") or "").strip().upper()
    property_obj.timezone = (post_data.get("timezone") or "UTC").strip()
    property_obj.website = (post_data.get("website") or "").strip() or None
    property_obj.parent_property = parent_property
    property_obj.is_active = bool(post_data.get("is_active"))

    if property_obj.pk and parent_property and property_obj.pk == parent_property.pk:
        raise ValueError("A property cannot be its own parent property.")

    property_obj.save()
    return property_obj


@login_required
def index(request):
    return render(request, "restaurant_menu/property/list.html", {"fields": _build_fields()})


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "GET":
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Invalid request method"}, status=405)
        return redirect("property_list")

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    try:
        with transaction.atomic():
            _save_property_from_post(Property(), request.POST)
        if is_ajax:
            return JsonResponse({"success": True, "message": "Property created successfully"})
        messages.success(request, "Property created successfully")
        return redirect("property_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error creating property: {exc}")
        return redirect("property_list")


@login_required
@require_http_methods(["POST"])
def update(request, pk):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    property_obj = get_object_or_404(Property, pk=pk)
    try:
        with transaction.atomic():
            _save_property_from_post(property_obj, request.POST)
        if is_ajax:
            return JsonResponse({"success": True, "message": "Property updated successfully"})
        messages.success(request, "Property updated successfully")
        return redirect("property_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error updating property: {exc}")
        return redirect("property_list")


@login_required
def edit(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    return JsonResponse(
        {
            "id": property_obj.pk,
            "property_code": property_obj.property_code,
            "property_name": property_obj.property_name,
            "property_type": property_obj.property_type,
            "address": property_obj.address,
            "city": property_obj.city,
            "state": property_obj.state,
            "country": property_obj.country,
            "postal_code": property_obj.postal_code,
            "phone": property_obj.phone,
            "email": property_obj.email,
            "gst_number": property_obj.gst_number,
            "currency": property_obj.currency,
            "timezone": property_obj.timezone,
            "website": property_obj.website,
            "parent_property": property_obj.parent_property_id,
            "is_active": property_obj.is_active,
        }
    )


@login_required
@require_http_methods(["POST"])
def delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    property_obj.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "Property deleted successfully"})

    messages.success(request, "Property deleted successfully")
    return redirect("property_list")


@login_required
def select(request):
    keyword = (request.GET.get("term") or request.GET.get("q") or "").strip()
    exclude_id = request.GET.get("exclude_id")

    queryset = Property.objects.all()

    if keyword:
        queryset = queryset.filter(property_name__icontains=keyword)
    if exclude_id:
        queryset = queryset.exclude(pk=exclude_id)

    queryset = queryset.order_by("-created_at")[:20]
    results = [{"id": item.pk, "text": f"{item.property_name} ({item.property_code})"} for item in queryset]

    return JsonResponse({"results": results})
