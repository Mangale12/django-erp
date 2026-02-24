from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import require_http_methods

from hotel_app.restaurant_menu.models import BillMaster
from hotel_app.restaurant_menu.selectors.bill_selector import BillSelector
from hotel_app.restaurant_menu.services.bill_service import BillService


def index(request):
    fields = [
        {"name": "property", "label": "Property", "type": "select", "url": reverse("property_select")},
        {"name": "outlet", "label": "Outlet", "type": "select", "url": reverse("outlet_select")},
        {"name": "bill_type", "label": "Bill Type", "type": "select", "url": reverse("bill_type_select")},
        {"name": "source_module", "label": "Source Module", "type": "select", "url": reverse("source_module_select")},
        {"name": "order", "label": "Order", "type": "select", "url": reverse("order_select")},
        {"name": "guest", "label": "Guest", "type": "select", "url": reverse("guest_select")},
        {"name": "room", "label": "Room", "type": "select", "url": reverse("room_select")},
        {"name": "folio", "label": "Folio", "type": "select", "url": reverse("folio_select")},
        {"name": "sub_total", "label": "Sub Total", "type": "number", "required": True, "step": "0.01", "min": 0},
        {"name": "discount_type", "label": "Discount Type", "type": "select", "url": reverse("discount_type_select")},
        {"name": "discount_value", "label": "Discount Value", "type": "number", "step": "0.01", "min": 0},
        {"name": "extra_charge_amount", "label": "Extra Charge", "type": "number", "step": "0.01", "min": 0},
        {"name": "service_charge_amount", "label": "Service Charge", "type": "number", "step": "0.01", "min": 0},
        {"name": "tax_type", "label": "Tax Type", "type": "select", "url": reverse("tax_type_select")},
        {"name": "round_off", "label": "Round Off", "type": "number", "step": "0.01"},
        {"name": "payment_status", "label": "Payment Status", "type": "static_select", "options": BillMaster.PAYMENT_STATUS_CHOICES},
        {"name": "bill_status", "label": "Bill Status", "type": "static_select", "options": BillMaster.BILL_STATUS_CHOICES},
    ]
    
    dynamic_sections = {
        "order_items": {
            "title": "Bill Items",
            "layout": "table",
            "min_items": 1,
            "max_items": 20,
            "add_label": "Add Item",
            "show_grand_total": True,
            "fields": [
                {"name": "menu_item", "class" : "menu_item", "label": "Menu Item", "type": "select", "required": True, "url": reverse("menu_item_select")},
                {"name": "quantity", "class" : "quantity", "label": "Qty", "type": "number", "required": True, "min": 1},
                {"name": "rate", "class" : "rate", "label": "Rate", "type": "number", "readonly": True},
                {"name": "gross_amount", "class" : "gross_amount", "label": "Gross Amount", "type": "number", "readonly": True},
                {"name": "discount_type", "class" : "discount_type", "label": "Discount Type", "type": "select", "url": reverse("discount_type_select")},
                {"name": "discount_value", "class" : "discount_value", "label": "Discount Value", "type": "number", "step": "0.01", "min": 0},
                {"name" : "net_amount", "class" : "net_amount", "label": "Net Amount", "type": "number", "readonly": True},
                {"name": "modifiers", "class" : "modifiers", "label": "Modifiers", "type": "multi_select", "url": reverse("modifier_select")},
                {"name": "is_complementary", "class" : "is_complementary", "label": "Is Complementary", "type": "checkbox"},
            ],
        }
    }
    return render(request, "restaurant_menu/bill_master/list.html", {"fields": fields, "dynamic_sections": dynamic_sections})


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "GET":
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Invalid request method"}, status=405)
        return redirect("bill_master_list")

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    bill_master, form = BillService.create(request.POST, user=request.user)

    if bill_master:
        if is_ajax:
            return JsonResponse({"success": True, "message": "Bill created successfully", "id": bill_master.id})
        messages.success(request, "Bill created successfully")
        return redirect("bill_master_list")

    error_text = "; ".join(
        [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
    ) or "Invalid bill data"
    if is_ajax:
        return JsonResponse({"success": False, "error": error_text}, status=400)
    messages.error(request, f"Error creating bill: {error_text}")
    return redirect("bill_master_list")


@require_http_methods(["POST"])
def update(request, pk):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    bill_master = get_object_or_404(BillSelector.get_all(), pk=pk)
    updated_bill, form = BillService.update(bill_master, request.POST)

    if updated_bill:
        if is_ajax:
            return JsonResponse({"success": True, "message": "Bill updated successfully", "id": updated_bill.id})
        messages.success(request, "Bill updated successfully")
        return redirect("bill_master_list")

    error_text = "; ".join(
        [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
    ) or "Invalid bill data"
    if is_ajax:
        return JsonResponse({"success": False, "error": error_text}, status=400)
    messages.error(request, f"Error updating bill: {error_text}")
    return redirect("bill_master_list")


def edit(request, pk):
    bill_master = get_object_or_404(BillSelector.get_all(), pk=pk)
    return JsonResponse(
        {
            "success": True,
            "data": {
                "id": bill_master.id,
                "bill_no": bill_master.bill_no,
                "property": bill_master.property_id,
                "outlet": bill_master.outlet_id,
                "bill_type": bill_master.bill_type_id,
                "source_module": bill_master.source_module_id,
                "order": bill_master.order_id,
                "guest": bill_master.guest_id,
                "room": bill_master.room_id,
                "stay": bill_master.stay_id,
                "folio": bill_master.folio_id,
                "sub_total": bill_master.sub_total,
                "discount_type": bill_master.discount_type_id,
                "discount_value": bill_master.discount_value,
                "extra_charge_amount": bill_master.extra_charge_amount,
                "service_charge_amount": bill_master.service_charge_amount,
                "tax_type": bill_master.tax_type_id,
                "round_off": bill_master.round_off,
                "payment_status": bill_master.payment_status,
                "bill_status": bill_master.bill_status,
            },
        }
    )


@require_http_methods(["POST"])
def delete(request, pk):
    bill_master = get_object_or_404(BillMaster, pk=pk)
    bill_master.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "Bill deleted successfully"})

    messages.success(request, "Bill deleted successfully")
    return redirect("bill_master_list")


def select(request):
    keyword = (request.GET.get("term") or request.GET.get("q") or "").strip()
    queryset = BillSelector.get_all()

    if keyword:
        queryset = queryset.filter(
            Q(bill_no__icontains=keyword)
            | Q(guest__name__icontains=keyword)
            | Q(room__room_number__icontains=keyword)
        )

    queryset = queryset.order_by("-created_at")[:20]
    results = [
        {
            "id": item.id,
            "text": f"{item.bill_no} | {item.grand_total or 0}",
        }
        for item in queryset
    ]
    return JsonResponse({"results": results})
