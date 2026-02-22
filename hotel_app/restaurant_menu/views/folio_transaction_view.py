from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from hotel_app.restaurant_menu.models import Folio, FolioTransaction


def _build_fields():
    folio_options = [(str(item.id), f"Folio #{item.id} - Stay #{item.stay_id}") for item in Folio.objects.order_by("-created_at")[:200]]
    return [
        {
            "name": "folio",
            "label": "Folio",
            "type": "static_select",
            "required": True,
            "options": folio_options,
        },
        {"name": "source_module_id", "label": "Source Module ID", "type": "text", "required": True},
        {"name": "reference_id", "label": "Reference ID (Bill ID)", "type": "number", "required": True},
        {"name": "debit_amount", "label": "Debit Amount", "type": "number", "required": True, "step": "0.01"},
        {"name": "credit_amount", "label": "Credit Amount", "type": "number", "required": True, "step": "0.01"},
        {"name": "transaction_date", "label": "Transaction Date", "type": "datetime", "required": True},
    ]


def _to_decimal(value, field_name):
    try:
        return Decimal(str(value or "0"))
    except (InvalidOperation, ValueError):
        raise ValueError(f"Invalid numeric value for {field_name}.")


def _recalculate_folio_totals(folio):
    aggregates = folio.transactions.aggregate(
        total_debit=Sum("debit_amount"),
        total_credit=Sum("credit_amount"),
    )
    folio.total_debit = aggregates.get("total_debit") or Decimal("0")
    folio.total_credit = aggregates.get("total_credit") or Decimal("0")
    folio.balance_amount = folio.total_debit - folio.total_credit
    folio.save(update_fields=["total_debit", "total_credit", "balance_amount", "updated_at"])


def _save_folio_transaction_from_post(trn_obj, post_data):
    folio_id = post_data.get("folio")
    if not folio_id:
        raise ValueError("Folio is required.")

    folio = get_object_or_404(Folio, pk=folio_id)
    trn_obj.folio = folio
    trn_obj.source_module_id = (post_data.get("source_module_id") or "").strip()
    trn_obj.reference_id = int(post_data.get("reference_id") or 0)
    trn_obj.debit_amount = _to_decimal(post_data.get("debit_amount"), "debit_amount")
    trn_obj.credit_amount = _to_decimal(post_data.get("credit_amount"), "credit_amount")
    trn_obj.transaction_date = post_data.get("transaction_date")
    trn_obj.save()
    _recalculate_folio_totals(folio)
    return trn_obj


@login_required
def index(request):
    return render(request, "restaurant_menu/folio_transaction/list.html", {"fields": _build_fields()})


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "GET":
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Invalid request method"}, status=405)
        return redirect("folio_transaction_list")

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    try:
        with transaction.atomic():
            _save_folio_transaction_from_post(FolioTransaction(), request.POST)
        if is_ajax:
            return JsonResponse({"success": True, "message": "Folio transaction created successfully"})
        messages.success(request, "Folio transaction created successfully")
        return redirect("folio_transaction_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error creating folio transaction: {exc}")
        return redirect("folio_transaction_list")


@login_required
@require_http_methods(["POST"])
def update(request, pk):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    trn_obj = get_object_or_404(FolioTransaction, pk=pk)
    previous_folio = trn_obj.folio
    try:
        with transaction.atomic():
            _save_folio_transaction_from_post(trn_obj, request.POST)
            if previous_folio_id := getattr(previous_folio, "id", None):
                if previous_folio_id != trn_obj.folio_id:
                    _recalculate_folio_totals(previous_folio)
        if is_ajax:
            return JsonResponse({"success": True, "message": "Folio transaction updated successfully"})
        messages.success(request, "Folio transaction updated successfully")
        return redirect("folio_transaction_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error updating folio transaction: {exc}")
        return redirect("folio_transaction_list")


@login_required
def edit(request, pk):
    trn_obj = get_object_or_404(FolioTransaction, pk=pk)
    payload = {
        "id": trn_obj.pk,
        "folio": trn_obj.folio_id,
        "source_module_id": trn_obj.source_module_id,
        "reference_id": trn_obj.reference_id,
        "debit_amount": float(trn_obj.debit_amount),
        "credit_amount": float(trn_obj.credit_amount),
        "transaction_date": trn_obj.transaction_date,
    }
    return JsonResponse({"success": True, "data": payload, **payload})


@login_required
@require_http_methods(["POST"])
def delete(request, pk):
    trn_obj = get_object_or_404(FolioTransaction, pk=pk)
    folio = trn_obj.folio
    trn_obj.delete()
    _recalculate_folio_totals(folio)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "Folio transaction deleted successfully"})

    messages.success(request, "Folio transaction deleted successfully")
    return redirect("folio_transaction_list")


@login_required
def select(request):
    keyword = (request.GET.get("term") or request.GET.get("q") or "").strip()

    queryset = FolioTransaction.objects.select_related("folio", "folio__stay").all()
    if keyword:
        queryset = queryset.filter(source_module_id__icontains=keyword)

    queryset = queryset.order_by("-created_at")[:20]
    results = [{"id": item.pk, "text": f"FTrn #{item.pk} - Folio #{item.folio_id}"} for item in queryset]
    return JsonResponse({"results": results})
