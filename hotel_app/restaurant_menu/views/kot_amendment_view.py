from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods

from hotel_app.restaurant_menu.models import KOTAmendment, KOTHeader, KOTLineItem, MenuItem, Order
from django.contrib.auth import get_user_model

User = get_user_model()


def _build_fields():
    manager_options = [(str(user.id), user.get_username()) for user in User.objects.filter(is_active=True).order_by("username")]
    return [
        {"name": "business_date", "label": "Business Date", "type": "date", "required": True},
        {"name": "kot", "label": "KOT", "type": "select", "required": True, "url": reverse("kot_header_select")},
        {"name": "kot_line_item", "label": "KOT Line", "type": "select", "url": reverse("kot_line_item_select")},
        {"name": "order", "label": "Order", "type": "select", "required": True, "url": reverse("order_select")},
        {"name": "original_item", "label": "Original Item", "type": "select", "required": True, "url": reverse("menu_item_select")},
        {"name": "new_item", "label": "New Item", "type": "select", "url": reverse("menu_item_select")},
        {"name": "action_type", "label": "Action Type", "type": "static_select", "required": True, "options": KOTAmendment.ACTION_TYPE_CHOICES},
        {"name": "old_quantity", "label": "Old Quantity", "type": "number", "step": "0.01", "min": "0"},
        {"name": "new_quantity", "label": "New Quantity", "type": "number", "step": "0.01", "min": "0"},
        {"name": "manager", "label": "Manager", "type": "static_select", "required": True, "options": manager_options},
        {"name": "reason_code", "label": "Reason Code", "type": "text", "required": True},
        {"name": "remarks", "label": "Remarks", "type": "textarea"},
        {"name": "timestamp_amended", "label": "Timestamp Amended", "type": "datetime"},
    ]


def _parse_timestamp(raw_value):
    if not raw_value:
        return timezone.now()
    parsed = parse_datetime(raw_value)
    if not parsed:
        return timezone.now()
    if timezone.is_naive(parsed):
        return timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed


def _save_amendment_from_post(amendment, post_data, user):
    amendment.business_date = post_data.get("business_date") or timezone.localdate()
    amendment.kot = get_object_or_404(KOTHeader, pk=post_data.get("kot"))
    amendment.kot_line_item = get_object_or_404(KOTLineItem, pk=post_data.get("kot_line_item")) if post_data.get("kot_line_item") else None
    amendment.order = get_object_or_404(Order, pk=post_data.get("order"))
    amendment.original_item = get_object_or_404(MenuItem, pk=post_data.get("original_item"))
    amendment.new_item = get_object_or_404(MenuItem, pk=post_data.get("new_item")) if post_data.get("new_item") else None
    amendment.action_type = post_data.get("action_type") or "ADDED"
    amendment.old_quantity = post_data.get("old_quantity") or 0
    amendment.new_quantity = post_data.get("new_quantity") or 0
    amendment.manager = get_object_or_404(User, pk=post_data.get("manager"))
    amendment.reason_code = post_data.get("reason_code") or ""
    amendment.remarks = post_data.get("remarks") or None
    amendment.timestamp_amended = _parse_timestamp(post_data.get("timestamp_amended"))
    amendment.amended_by = user
    amendment.save()
    return amendment


@login_required
def index(request):
    return render(request, "restaurant_menu/kot_amendment/list.html", {"fields": _build_fields()})


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "GET":
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Invalid request method"}, status=405)
        return redirect("kot_amendment_list")

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    try:
        with transaction.atomic():
            _save_amendment_from_post(KOTAmendment(), request.POST, request.user)
        if is_ajax:
            return JsonResponse({"success": True, "message": "KOT Amendment created successfully"})
        messages.success(request, "KOT Amendment created successfully")
        return redirect("kot_amendment_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error creating KOT Amendment: {exc}")
        return redirect("kot_amendment_list")


@login_required
@require_http_methods(["POST"])
def update(request, pk):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    amendment = get_object_or_404(KOTAmendment, pk=pk)
    try:
        with transaction.atomic():
            _save_amendment_from_post(amendment, request.POST, request.user)
        if is_ajax:
            return JsonResponse({"success": True, "message": "KOT Amendment updated successfully"})
        messages.success(request, "KOT Amendment updated successfully")
        return redirect("kot_amendment_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error updating KOT Amendment: {exc}")
        return redirect("kot_amendment_list")


@login_required
def edit(request, pk):
    amendment = get_object_or_404(KOTAmendment, pk=pk)
    return JsonResponse(
        {
            "id": amendment.pk,
            "business_date": amendment.business_date.isoformat() if amendment.business_date else "",
            "kot": amendment.kot_id,
            "kot_line_item": amendment.kot_line_item_id,
            "order": amendment.order_id,
            "original_item": amendment.original_item_id,
            "new_item": amendment.new_item_id,
            "action_type": amendment.action_type,
            "old_quantity": str(amendment.old_quantity),
            "new_quantity": str(amendment.new_quantity),
            "manager": amendment.manager_id,
            "reason_code": amendment.reason_code,
            "remarks": amendment.remarks,
            "timestamp_amended": amendment.timestamp_amended.strftime("%Y-%m-%dT%H:%M") if amendment.timestamp_amended else "",
        }
    )


@login_required
@require_http_methods(["POST"])
def delete(request, pk):
    amendment = get_object_or_404(KOTAmendment, pk=pk)
    amendment.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "KOT Amendment deleted successfully"})

    messages.success(request, "KOT Amendment deleted successfully")
    return redirect("kot_amendment_list")


@login_required
def select(request):
    keyword = (request.GET.get("term") or request.GET.get("q") or "").strip()
    queryset = KOTAmendment.objects.select_related("kot", "order").all()

    if keyword:
        queryset = queryset.filter(reason_code__icontains=keyword)

    queryset = queryset.order_by("-timestamp_amended")[:20]
    results = [
        {
            "id": item.pk,
            "text": f"{item.pk} | {item.get_action_type_display()} | {item.kot.kot_number if item.kot else '-'}",
        }
        for item in queryset
    ]
    return JsonResponse({"results": results})
