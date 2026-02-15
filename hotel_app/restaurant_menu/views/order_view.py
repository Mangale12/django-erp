import re
from collections import defaultdict
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from hotel_app.restaurant_menu.models import (
    MenuItem,
    Modifier,
    Order,
    OrderItem,
    OrderItemModifier,
)


def _to_decimal(value, fallback=Decimal("0.00")):
    try:
        if value in (None, ""):
            return fallback
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return fallback


def _next_order_number():
    base = timezone.now().strftime("ORD%Y%m%d%H%M%S")
    candidate = base
    suffix = 1
    while Order.objects.filter(order_number=candidate).exists():
        candidate = f"{base}{suffix:02d}"
        suffix += 1
    return candidate


def _parse_order_items(post_data):
    pattern = re.compile(r"^order_items\[(\d+)\]\[([^\]]+)\](\[\])?$")
    grouped = defaultdict(dict)

    for key in post_data.keys():
        match = pattern.match(key)
        if not match:
            continue

        row_index = int(match.group(1))
        field_name = match.group(2)
        is_list = bool(match.group(3))

        if is_list:
            grouped[row_index][field_name] = post_data.getlist(key)
        else:
            grouped[row_index][field_name] = post_data.get(key)

    parsed_rows = []
    for row_index in sorted(grouped.keys()):
        row = grouped[row_index]
        if row.get("menu_item"):
            parsed_rows.append(row)
    return parsed_rows


def _save_order_items(order, items_payload):
    order.order_items.all().delete()

    for row in items_payload:
        menu_item = get_object_or_404(MenuItem, pk=row.get("menu_item"))
        quantity = int(row.get("quantity") or 1)
        unit_price = _to_decimal(row.get("unit_price"), fallback=menu_item.price or Decimal("0.00"))
        total_price = _to_decimal(row.get("total_price"), fallback=unit_price * quantity)
        item_status = row.get("status") or "ordered"

        order_item = OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            order_item_status=item_status,
        )

        modifier_ids = row.get("modifiers", [])
        if modifier_ids:
            valid_modifiers = Modifier.objects.filter(id__in=modifier_ids, menu_item=menu_item)
            OrderItemModifier.objects.bulk_create(
                [
                    OrderItemModifier(order_item=order_item, modifier=modifier, quantity=1)
                    for modifier in valid_modifiers
                ]
            )


def index(request):
    fields = [
        {"name": "table", "label": "Table", "type": "select", "required": True, "url": reverse("table_setup_select")},
        {"name": "guest_count", "label": "Guest Count", "type": "number", "required": True, "min": 1},
        {"name": "guest_name", "label": "Guest Name", "type": "text", "required": True},
        {"name": "room", "label": "Room", "type": "select", "url": reverse("room_select")},
        {"name": "order_status", "label": "Order Status", "type": "static_select", "required": True, "options": Order.ORDER_STATUS},
    ]

    dynamic_sections = {
        "order_items": {
            "title": "Order Items",
            "layout": "table",
            "min_items": 1,
            "max_items": 20,
            "add_label": "Add Item",
            "show_grand_total": True,
            "fields": [
                {"name": "menu_item", "class" : "menu_item", "label": "Menu Item", "type": "select", "required": True, "url": reverse("menu_item_select")},
                {"name": "quantity", "class" : "quantity", "label": "Qty", "type": "number", "required": True, "min": 1},
                {"name": "unit_price", "class" : "unit_price", "label": "Unit Price", "type": "number", "readonly": True},
                {"name": "total_price", "class" : "total_price", "label": "Total", "type": "number", "readonly": True},
                {"name": "modifiers", "class" : "modifiers", "label": "Modifiers", "type": "multi_select", "url": reverse("modifier_select")},
                {"name": "status", "class" : "status", "label": "Status", "type": "select_static", "values": OrderItem.ORDER_ITEM_STATUS},
            ],
        }
    }

    return render(
        request,
        "restaurant_menu/order/list.html",
        {
            "fields": fields,
            "dynamic_sections": dynamic_sections,
        },
    )


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "GET":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    try:
        with transaction.atomic():
            order = Order.objects.create(
                order_number=_next_order_number(),
                table_id=request.POST.get("table") or None,
                user=request.user if request.user.is_authenticated else None,
                guest_count=int(request.POST.get("guest_count") or 1),
                room_id=request.POST.get("room") or None,
                guest_name=request.POST.get("guest_name") or "Guest",
                order_status=request.POST.get("order_status") or "pending",
            )

            order_items_payload = _parse_order_items(request.POST)
            _save_order_items(order, order_items_payload)

        if is_ajax:
            return JsonResponse({"success": True, "message": "Order created successfully", "id": order.id})

        messages.success(request, "Order created successfully")
        return redirect("order_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error creating order: {exc}")
        return redirect("order_list")


@require_http_methods(["POST"])
def update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    try:
        with transaction.atomic():
            order.table_id = request.POST.get("table") or None
            order.guest_count = int(request.POST.get("guest_count") or 1)
            order.room_id = request.POST.get("room") or None
            order.guest_name = request.POST.get("guest_name") or order.guest_name
            order.order_status = request.POST.get("order_status") or order.order_status
            order.save()

            order_items_payload = _parse_order_items(request.POST)
            _save_order_items(order, order_items_payload)

        if is_ajax:
            return JsonResponse({"success": True, "message": "Order updated successfully", "id": order.id})

        messages.success(request, "Order updated successfully")
        return redirect("order_list")
    
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error updating order: {exc}")
        return redirect("order_list")


def edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return JsonResponse(
        {
            "success": True,
            "data": {
                "id": order.id,
                "table": order.table_id,
                "guest_count": order.guest_count,
                "guest_name": order.guest_name,
                "room": order.room_id,
                "order_status": order.order_status,
            },
        }
    )


@require_http_methods(["POST"])
def delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "Order deleted successfully"})

    messages.success(request, "Order deleted successfully")
    return redirect("order_list")


def show(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "restaurant_menu/order/show.html", {"order": order})


def select(request):
    keyword = (request.GET.get("term") or request.GET.get("q") or "").strip()
    qs = Order.objects.all()

    if keyword:
        qs = qs.filter(guest_name__icontains=keyword)

    qs = qs.order_by("-created_at")[:20]
    results = [{"id": item.id, "text": f"{item.order_number} - {item.guest_name}"} for item in qs]
    return JsonResponse({"results": results})


def menu_item_details(request):
    menu_item_id = request.GET.get("menu_item_id")
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
    modifiers = Modifier.objects.filter(menu_item=menu_item, is_active=True).order_by("name")

    return JsonResponse(
        {
            "id": menu_item.id,
            "unit_price": str(menu_item.price or Decimal("0.00")),
            "modifiers": [
                {
                    "id": modifier.id,
                    "text": f"{modifier.name} (+{modifier.extra_price})"
                    if modifier.extra_price
                    else modifier.name,
                }
                for modifier in modifiers
            ],
        }
    )
