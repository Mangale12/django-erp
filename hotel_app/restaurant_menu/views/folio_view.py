from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from hotel_app.reception.models import Stay
from hotel_app.restaurant_menu.models import Folio


def _build_fields():
    stay_options = [
        (
            str(item.id),
            f"Stay #{item.id} - {getattr(item.guest, 'name', 'Guest')}",
        )
        for item in Stay.objects.select_related("guest").order_by("-created_at")[:200]
    ]
    return [
        {
            "name": "stay",
            "label": "Stay",
            "type": "static_select",
            "required": True,
            "options": stay_options,
        },
        {"name": "total_debit", "label": "Total Debit", "type": "number", "required": True, "step": "0.01"},
        {"name": "total_credit", "label": "Total Credit", "type": "number", "required": True, "step": "0.01"},
        {
            "name": "balance_amount",
            "label": "Balance Amount (Auto)",
            "type": "number",
            "attributes": {"readonly": "readonly"},
            "step": "0.01",
        },
        {
            "name": "folio_status",
            "label": "Folio Status",
            "type": "static_select",
            "required": True,
            "options": Folio.FOLIO_STATUS_CHOICES,
        },
    ]


def _to_decimal(value, field_name):
    try:
        return Decimal(str(value or "0"))
    except (InvalidOperation, ValueError):
        raise ValueError(f"Invalid numeric value for {field_name}.")


def _save_folio_from_post(folio_obj, post_data):
    stay_id = post_data.get("stay")
    if not stay_id:
        raise ValueError("Stay is required.")

    folio_obj.stay = get_object_or_404(Stay, pk=stay_id)
    folio_obj.total_debit = _to_decimal(post_data.get("total_debit"), "total_debit")
    folio_obj.total_credit = _to_decimal(post_data.get("total_credit"), "total_credit")
    folio_obj.folio_status = post_data.get("folio_status") or "OPEN"
    folio_obj.save()
    return folio_obj


@login_required
def index(request):
    return render(request, "restaurant_menu/folio/list.html", {"fields": _build_fields()})


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "GET":
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Invalid request method"}, status=405)
        return redirect("folio_list")

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    try:
        with transaction.atomic():
            _save_folio_from_post(Folio(), request.POST)
        if is_ajax:
            return JsonResponse({"success": True, "message": "Folio created successfully"})
        messages.success(request, "Folio created successfully")
        return redirect("folio_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error creating folio: {exc}")
        return redirect("folio_list")


@login_required
@require_http_methods(["POST"])
def update(request, pk):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    folio_obj = get_object_or_404(Folio, pk=pk)
    try:
        with transaction.atomic():
            _save_folio_from_post(folio_obj, request.POST)
        if is_ajax:
            return JsonResponse({"success": True, "message": "Folio updated successfully"})
        messages.success(request, "Folio updated successfully")
        return redirect("folio_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error updating folio: {exc}")
        return redirect("folio_list")


@login_required
def edit(request, pk):
    folio_obj = get_object_or_404(Folio, pk=pk)
    payload = {
        "id": folio_obj.pk,
        "stay": folio_obj.stay_id,
        "total_debit": float(folio_obj.total_debit),
        "total_credit": float(folio_obj.total_credit),
        "balance_amount": float(folio_obj.balance_amount),
        "folio_status": folio_obj.folio_status,
    }
    return JsonResponse({"success": True, "data": payload, **payload})


@login_required
@require_http_methods(["POST"])
def delete(request, pk):
    folio_obj = get_object_or_404(Folio, pk=pk)
    folio_obj.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "Folio deleted successfully"})

    messages.success(request, "Folio deleted successfully")
    return redirect("folio_list")


@login_required
def select(request):
    keyword = (request.GET.get("term") or request.GET.get("q") or "").strip()

    queryset = Folio.objects.select_related("stay", "stay__guest").all()
    if keyword:
        queryset = queryset.filter(stay__guest__name__icontains=keyword)

    queryset = queryset.order_by("-created_at")[:20]
    results = [
        {"id": item.pk, "text": f"Folio #{item.pk} - Stay #{item.stay_id}"}
        for item in queryset
    ]
    return JsonResponse({"results": results})
