from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods

from hotel_app.restaurant_menu.models import KDSLog, KOTLineItem, Kitchen, KitchenStation


def _build_fields():
    return [
        {"name": "business_date", "label": "Business Date", "type": "date", "required": True},
        {"name": "kot_line", "label": "KOT Line", "type": "select", "required": True, "url": reverse("kot_line_item_select")},
        {"name": "kitchen", "label": "Kitchen", "type": "select", "required": True, "url": reverse("kitchen_select")},
        {"name": "station", "label": "Station", "type": "select", "required": True, "url": reverse("kitchen_station_select")},
        {"name": "action_taken", "label": "Action Taken", "type": "static_select", "required": True, "options": KDSLog.ACTION_CHOICES},
        {"name": "action_timestamp", "label": "Action Timestamp", "type": "datetime"},
        {"name": "delay_reason", "label": "Delay Reason", "type": "textarea"},
        {"name": "device_id", "label": "Device ID", "type": "text"},
        {"name": "ip_address", "label": "IP Address", "type": "text"},
    ]


def _parse_action_timestamp(raw_value):
    if not raw_value:
        return timezone.now()

    parsed = parse_datetime(raw_value)
    if not parsed:
        return timezone.now()

    if timezone.is_naive(parsed):
        return timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed


def _save_kds_log_from_post(kds_log, post_data, user):
    kds_log.business_date = post_data.get("business_date") or timezone.localdate()
    kds_log.kot_line = get_object_or_404(KOTLineItem, pk=post_data.get("kot_line"))
    kds_log.kitchen = get_object_or_404(Kitchen, pk=post_data.get("kitchen"))
    kds_log.station = get_object_or_404(KitchenStation, pk=post_data.get("station"))
    kds_log.action_taken = post_data.get("action_taken") or "FIRE"
    kds_log.action_by = user
    kds_log.action_timestamp = _parse_action_timestamp(post_data.get("action_timestamp"))
    kds_log.delay_reason = post_data.get("delay_reason") or None
    kds_log.device_id = post_data.get("device_id") or None
    kds_log.ip_address = post_data.get("ip_address") or None
    kds_log.save()
    return kds_log


@login_required
def index(request):
    return render(request, "restaurant_menu/kds_log/list.html", {"fields": _build_fields()})


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "GET":
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Invalid request method"}, status=405)
        return redirect("kds_log_list")

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    try:
        with transaction.atomic():
            _save_kds_log_from_post(KDSLog(), request.POST, request.user)

        if is_ajax:
            return JsonResponse({"success": True, "message": "KDS Log created successfully"})
        messages.success(request, "KDS Log created successfully")
        return redirect("kds_log_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error creating KDS Log: {exc}")
        return redirect("kds_log_list")


@login_required
@require_http_methods(["POST"])
def update(request, pk):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    kds_log = get_object_or_404(KDSLog, pk=pk)
    try:
        with transaction.atomic():
            _save_kds_log_from_post(kds_log, request.POST, request.user)

        if is_ajax:
            return JsonResponse({"success": True, "message": "KDS Log updated successfully"})
        messages.success(request, "KDS Log updated successfully")
        return redirect("kds_log_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error updating KDS Log: {exc}")
        return redirect("kds_log_list")


@login_required
def edit(request, pk):
    kds_log = get_object_or_404(KDSLog, pk=pk)
    return JsonResponse(
        {
            "id": kds_log.pk,
            "business_date": kds_log.business_date.isoformat() if kds_log.business_date else "",
            "kot_line": kds_log.kot_line_id,
            "kitchen": kds_log.kitchen_id,
            "station": kds_log.station_id,
            "action_taken": kds_log.action_taken,
            "action_timestamp": kds_log.action_timestamp.strftime("%Y-%m-%dT%H:%M") if kds_log.action_timestamp else "",
            "delay_reason": kds_log.delay_reason,
            "device_id": kds_log.device_id,
            "ip_address": kds_log.ip_address,
        }
    )


@login_required
@require_http_methods(["POST"])
def delete(request, pk):
    kds_log = get_object_or_404(KDSLog, pk=pk)
    kds_log.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "KDS Log deleted successfully"})

    messages.success(request, "KDS Log deleted successfully")
    return redirect("kds_log_list")


@login_required
def select(request):
    keyword = (request.GET.get("term") or request.GET.get("q") or "").strip()
    queryset = KDSLog.objects.select_related("kot_line").all()

    if keyword:
        queryset = queryset.filter(action_taken__icontains=keyword)

    queryset = queryset.order_by("-action_timestamp")[:20]
    results = [
        {
            "id": item.pk,
            "text": f"{item.pk} | {item.get_action_taken_display()} | Line {item.kot_line_id}",
        }
        for item in queryset
    ]
    return JsonResponse({"results": results})
