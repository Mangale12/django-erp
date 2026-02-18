from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods

from hotel_app.restaurant_menu.models import KOTCourseControl, KOTHeader

User = get_user_model()


def _build_fields():
    fired_by_options = [(str(user.id), user.get_username()) for user in User.objects.filter(is_active=True).order_by("username")]
    return [
        {"name": "kot", "label": "KOT", "type": "select", "required": True, "url": reverse("kot_header_select")},
        {"name": "course_number", "label": "Course Number", "type": "number", "required": True, "min": 1},
        {"name": "fire_status", "label": "Fire Status", "type": "static_select", "required": True, "options": KOTCourseControl.FIRE_STATUS_CHOICES},
        {"name": "hold_until_time", "label": "Hold Until Time", "type": "time"},
        {"name": "fired_by", "label": "Fired By", "type": "static_select", "options": fired_by_options},
        {"name": "fired_timestamp", "label": "Fired Timestamp", "type": "datetime"},
    ]


def _parse_fired_timestamp(raw_value):
    if not raw_value:
        return None
    parsed = parse_datetime(raw_value)
    if not parsed:
        return None
    if timezone.is_naive(parsed):
        return timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed


def _save_course_control_from_post(control, post_data):
    control.kot = get_object_or_404(KOTHeader, pk=post_data.get("kot"))
    control.course_number = post_data.get("course_number") or 1
    control.fire_status = post_data.get("fire_status") or "HOLD"
    control.hold_until_time = post_data.get("hold_until_time") or None
    control.fired_by = get_object_or_404(User, pk=post_data.get("fired_by")) if post_data.get("fired_by") else None
    control.fired_timestamp = _parse_fired_timestamp(post_data.get("fired_timestamp"))

    if control.fire_status == "FIRED" and not control.fired_timestamp:
        control.fired_timestamp = timezone.now()

    control.save()
    return control


@login_required
def index(request):
    return render(request, "restaurant_menu/kot_course_control/list.html", {"fields": _build_fields()})


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "GET":
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Invalid request method"}, status=405)
        return redirect("kot_course_control_list")

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    try:
        with transaction.atomic():
            _save_course_control_from_post(KOTCourseControl(), request.POST)
        if is_ajax:
            return JsonResponse({"success": True, "message": "KOT Course Control created successfully"})
        messages.success(request, "KOT Course Control created successfully")
        return redirect("kot_course_control_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error creating KOT Course Control: {exc}")
        return redirect("kot_course_control_list")


@login_required
@require_http_methods(["POST"])
def update(request, pk):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    control = get_object_or_404(KOTCourseControl, pk=pk)
    try:
        with transaction.atomic():
            _save_course_control_from_post(control, request.POST)
        if is_ajax:
            return JsonResponse({"success": True, "message": "KOT Course Control updated successfully"})
        messages.success(request, "KOT Course Control updated successfully")
        return redirect("kot_course_control_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error updating KOT Course Control: {exc}")
        return redirect("kot_course_control_list")


@login_required
def edit(request, pk):
    control = get_object_or_404(KOTCourseControl, pk=pk)
    return JsonResponse(
        {
            "id": control.pk,
            "kot": control.kot_id,
            "course_number": control.course_number,
            "fire_status": control.fire_status,
            "hold_until_time": control.hold_until_time.strftime("%H:%M") if control.hold_until_time else "",
            "fired_by": control.fired_by_id,
            "fired_timestamp": control.fired_timestamp.strftime("%Y-%m-%dT%H:%M") if control.fired_timestamp else "",
        }
    )


@login_required
@require_http_methods(["POST"])
def delete(request, pk):
    control = get_object_or_404(KOTCourseControl, pk=pk)
    control.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "KOT Course Control deleted successfully"})

    messages.success(request, "KOT Course Control deleted successfully")
    return redirect("kot_course_control_list")


@login_required
def select(request):
    keyword = (request.GET.get("term") or request.GET.get("q") or "").strip()
    queryset = KOTCourseControl.objects.select_related("kot").all()

    if keyword:
        queryset = queryset.filter(kot__kot_number__icontains=keyword)

    queryset = queryset.order_by("-course_control_id")[:20]
    results = [
        {
            "id": item.pk,
            "text": f"{item.kot.kot_number if item.kot else '-'} | Course {item.course_number} | {item.get_fire_status_display()}",
        }
        for item in queryset
    ]
    return JsonResponse({"results": results})
