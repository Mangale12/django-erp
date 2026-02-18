from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import require_http_methods

from hotel_app.restaurant_menu.models import KOTHeader, KOTLineItem, KitchenStation, MenuItem


def _build_fields():
    return [
        {"name": "kot", "label": "KOT Header", "type": "select", "required": True, "url": reverse("kot_header_select")},
        {"name": "item", "label": "Menu Item", "type": "select", "required": True, "url": reverse("menu_item_select")},
        {"name": "item_code", "label": "Item Code", "type": "text"},
        {"name": "item_name_snapshot", "label": "Item Name Snapshot", "type": "text"},
        {
            "name": "quantity",
            "label": "Quantity",
            "type": "number",
            "required": True,
            "step": "0.01",
            "min": "0.01",
        },
        {"name": "uom", "label": "UOM", "type": "text", "required": True},
        {"name": "course_number", "label": "Course Number", "type": "number", "min": 1},
        {"name": "fire_sequence", "label": "Fire Sequence", "type": "number", "min": 1},
        {"name": "priority_level", "label": "Priority Level", "type": "static_select", "options": KOTLineItem.PRIORITY_CHOICES},
        {"name": "item_status", "label": "Item Status", "type": "static_select", "options": KOTLineItem.STATUS_CHOICES},
        {"name": "modifiers_text", "label": "Modifiers", "type": "textarea"},
        {"name": "cooking_instruction", "label": "Cooking Instruction", "type": "textarea"},
        {"name": "allergy_notes", "label": "Allergy Notes", "type": "textarea"},
        {"name": "station", "label": "Kitchen Station", "type": "select", "url": reverse("kitchen_station_select")},
        {"name": "is_complimentary", "label": "Complimentary", "type": "checkbox"},
        {"name": "expected_prep_time_minutes", "label": "Expected Prep Time (mins)", "type": "number", "min": 0},
        {"name": "is_bounced", "label": "Bounced", "type": "checkbox"},
        {"name": "bounce_reason", "label": "Bounce Reason", "type": "textarea"},
        {"name": "cancellation_reason_code", "label": "Cancellation Code", "type": "text"},
    ]


def _save_line_item_from_post(line_item, post_data):
    item_id = post_data.get("item")
    item = get_object_or_404(MenuItem, pk=item_id) if item_id else None

    line_item.kot = get_object_or_404(KOTHeader, pk=post_data.get("kot"))
    line_item.item = item
    line_item.item_code = post_data.get("item_code") or (item.code if item else None)
    line_item.item_name_snapshot = post_data.get("item_name_snapshot") or (item.name if item else None)
    line_item.quantity = post_data.get("quantity") or 1
    line_item.uom = post_data.get("uom") or "Nos"
    line_item.course_number = post_data.get("course_number") or 1
    line_item.fire_sequence = post_data.get("fire_sequence") or 1
    line_item.priority_level = post_data.get("priority_level") or "NORMAL"
    line_item.item_status = post_data.get("item_status") or "PENDING"
    line_item.modifiers_text = post_data.get("modifiers_text") or None
    line_item.cooking_instruction = post_data.get("cooking_instruction") or None
    line_item.allergy_notes = post_data.get("allergy_notes") or None
    line_item.station = get_object_or_404(KitchenStation, pk=post_data.get("station")) if post_data.get("station") else None
    line_item.is_complimentary = bool(post_data.get("is_complimentary"))
    line_item.expected_prep_time_minutes = post_data.get("expected_prep_time_minutes") or 0
    line_item.is_bounced = bool(post_data.get("is_bounced"))
    line_item.bounce_reason = post_data.get("bounce_reason") or None
    line_item.cancellation_reason_code = post_data.get("cancellation_reason_code") or None
    line_item.save()
    return line_item


def index(request):
    return render(request, "restaurant_menu/kot_line_item/list.html", {"fields": _build_fields()})


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "GET":
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Invalid request method"}, status=405)
        return render(request, "restaurant_menu/kot_line_item/form.html")

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    try:
        with transaction.atomic():
            _save_line_item_from_post(KOTLineItem(), request.POST)

        if is_ajax:
            return JsonResponse({"success": True, "message": "KOT Line Item created successfully"})

        messages.success(request, "KOT Line Item created successfully")
        return redirect("kot_line_item_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error creating KOT Line Item: {exc}")
        return redirect("kot_line_item_list")


@require_http_methods(["POST"])
def update(request, pk):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    line_item = get_object_or_404(KOTLineItem, pk=pk)
    try:
        with transaction.atomic():
            _save_line_item_from_post(line_item, request.POST)

        if is_ajax:
            return JsonResponse({"success": True, "message": "KOT Line Item updated successfully"})

        messages.success(request, "KOT Line Item updated successfully")
        return redirect("kot_line_item_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error updating KOT Line Item: {exc}")
        return redirect("kot_line_item_list")


def edit(request, pk):
    line_item = get_object_or_404(KOTLineItem, pk=pk)
    return JsonResponse(
        {
            "id": line_item.id,
            "kot": line_item.kot_id,
            "item": line_item.item_id,
            "item_code": line_item.item_code,
            "item_name_snapshot": line_item.item_name_snapshot,
            "quantity": str(line_item.quantity),
            "uom": line_item.uom,
            "course_number": line_item.course_number,
            "fire_sequence": line_item.fire_sequence,
            "priority_level": line_item.priority_level,
            "item_status": line_item.item_status,
            "modifiers_text": line_item.modifiers_text,
            "cooking_instruction": line_item.cooking_instruction,
            "allergy_notes": line_item.allergy_notes,
            "station": line_item.station_id,
            "is_complimentary": line_item.is_complimentary,
            "expected_prep_time_minutes": line_item.expected_prep_time_minutes,
            "is_bounced": line_item.is_bounced,
            "bounce_reason": line_item.bounce_reason,
            "cancellation_reason_code": line_item.cancellation_reason_code,
        }
    )


@require_http_methods(["POST"])
def delete(request, pk):
    line_item = get_object_or_404(KOTLineItem, pk=pk)
    line_item.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "KOT Line Item deleted successfully"})

    messages.success(request, "KOT Line Item deleted successfully")
    return redirect("kot_line_item_list")


def select(request):
    keyword = (request.GET.get("term") or request.GET.get("q") or "").strip()
    qs = KOTLineItem.objects.select_related("kot", "item").all()

    if keyword:
        qs = qs.filter(item_name_snapshot__icontains=keyword)

    qs = qs.order_by("-created_at")[:20]
    results = [
        {
            "id": item.id,
            "text": f"{item.kot.kot_number if item.kot else '-'} | {item.item_name_snapshot or (item.item.name if item.item else '-')}",
        }
        for item in qs
    ]
    return JsonResponse({"results": results})
