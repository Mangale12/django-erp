from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods

from hotel_app.restaurant_menu.models import KOTHeader, KOTReprintLog

User = get_user_model()


def _build_fields():
    user_options = [(str(user.id), user.get_username()) for user in User.objects.filter(is_active=True).order_by("username")]
    return [
        {"name": "kot", "label": "KOT", "type": "select", "required": True, "url": reverse("kot_header_select")},
        {"name": "reprinted_by", "label": "Reprinted By", "type": "static_select", "required": True, "options": user_options},
        {"name": "reprint_timestamp", "label": "Reprint Timestamp", "type": "datetime"},
        {"name": "reason", "label": "Reason", "type": "textarea", "required": True},
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


def _save_reprint_log_from_post(reprint_log, post_data):
    reprint_log.kot = get_object_or_404(KOTHeader, pk=post_data.get("kot"))
    reprint_log.reprinted_by = get_object_or_404(User, pk=post_data.get("reprinted_by"))
    reprint_log.reprint_timestamp = _parse_timestamp(post_data.get("reprint_timestamp"))
    reprint_log.reason = post_data.get("reason") or ""
    reprint_log.save()
    return reprint_log


@login_required
def index(request):
    return render(request, "restaurant_menu/kot_reprint_log/list.html", {"fields": _build_fields()})


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "GET":
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Invalid request method"}, status=405)
        return redirect("kot_reprint_log_list")

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    try:
        with transaction.atomic():
            _save_reprint_log_from_post(KOTReprintLog(), request.POST)
        if is_ajax:
            return JsonResponse({"success": True, "message": "KOT Reprint Log created successfully"})
        messages.success(request, "KOT Reprint Log created successfully")
        return redirect("kot_reprint_log_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error creating KOT Reprint Log: {exc}")
        return redirect("kot_reprint_log_list")


@login_required
@require_http_methods(["POST"])
def update(request, pk):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    reprint_log = get_object_or_404(KOTReprintLog, pk=pk)
    try:
        with transaction.atomic():
            _save_reprint_log_from_post(reprint_log, request.POST)
        if is_ajax:
            return JsonResponse({"success": True, "message": "KOT Reprint Log updated successfully"})
        messages.success(request, "KOT Reprint Log updated successfully")
        return redirect("kot_reprint_log_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error updating KOT Reprint Log: {exc}")
        return redirect("kot_reprint_log_list")


@login_required
def edit(request, pk):
    reprint_log = get_object_or_404(KOTReprintLog, pk=pk)
    return JsonResponse(
        {
            "id": reprint_log.pk,
            "kot": reprint_log.kot_id,
            "reprinted_by": reprint_log.reprinted_by_id,
            "reprint_timestamp": reprint_log.reprint_timestamp.strftime("%Y-%m-%dT%H:%M") if reprint_log.reprint_timestamp else "",
            "reason": reprint_log.reason,
        }
    )


@login_required
@require_http_methods(["POST"])
def delete(request, pk):
    reprint_log = get_object_or_404(KOTReprintLog, pk=pk)
    reprint_log.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "KOT Reprint Log deleted successfully"})

    messages.success(request, "KOT Reprint Log deleted successfully")
    return redirect("kot_reprint_log_list")


@login_required
def select(request):
    keyword = (request.GET.get("term") or request.GET.get("q") or "").strip()
    queryset = KOTReprintLog.objects.select_related("kot").all()

    if keyword:
        queryset = queryset.filter(kot__kot_number__icontains=keyword)

    queryset = queryset.order_by("-reprint_timestamp")[:20]
    results = [
        {
            "id": item.pk,
            "text": f"{item.kot.kot_number if item.kot else '-'} | {item.reprint_timestamp}",
        }
        for item in queryset
    ]
    return JsonResponse({"results": results})
