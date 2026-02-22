from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import require_http_methods

from hotel_app.reception.forms.stay_form import StayForm
from hotel_app.reception.models import Stay


def index(request):
    fields = [
        {"name": "guest", "label": "Guest", "type": "select", "required": True, "url": reverse("guest_select")},
        {"name": "booking", "label": "Booking", "type": "select", "required": False, "url": reverse("booking_select")},
        {"name": "check_in", "label": "Check In", "type": "select", "required": False, "url": reverse("checkin_select")},
        {"name": "check_out", "label": "Check Out", "type": "select", "required": False, "url": reverse("check_out_select")},
        {"name": "room", "label": "Room", "type": "select", "required": False, "url": reverse("room_select")},
        {"name": "check_in_date", "label": "Check In Date", "type": "datetime", "required": True},
        {"name": "expected_check_out_date", "label": "Expected Check Out Date", "type": "datetime"},
        {"name": "actual_check_out_date", "label": "Actual Check Out Date", "type": "datetime"},
        {
            "name": "stay_status",
            "label": "Stay Status",
            "type": "static_select",
            "required": True,
            "options": Stay.STAY_STATUS_CHOICES,
        },
        {"name": "remarks", "label": "Remarks", "type": "textarea"},
    ]
    return render(request, "reception/stay/index.html", {"fields": fields})


@require_http_methods(["GET", "POST"])
def create(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if request.method == "POST":
        form = StayForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                if is_ajax:
                    return JsonResponse({"success": True, "message": "Stay created successfully"})
                messages.success(request, "Stay created successfully")
                return redirect("stay_list")
            except Exception as exc:
                if is_ajax:
                    return JsonResponse({"success": False, "error": str(exc)}, status=500)
                messages.error(request, f"Error: {exc}")
        else:
            if is_ajax:
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
            return render(request, "reception/stay/form.html", {"form": form})

    return render(request, "reception/stay/form.html", {"form": StayForm()})


def edit(request, pk):
    stay = get_object_or_404(Stay, pk=pk)
    return JsonResponse(
        {
            "success": True,
            "data": {
                "id": stay.stay_id,
                "stay_id": stay.stay_id,
                "guest": stay.guest_id,
                "booking": stay.booking_id,
                "check_in": stay.check_in_id,
                "check_out": stay.check_out_id,
                "room": stay.room_id,
                "check_in_date": stay.check_in_date,
                "expected_check_out_date": stay.expected_check_out_date,
                "actual_check_out_date": stay.actual_check_out_date,
                "stay_status": stay.stay_status,
                "remarks": stay.remarks,
            },
        }
    )


def update(request, pk):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

    stay = get_object_or_404(Stay, pk=pk)
    form = StayForm(request.POST, instance=stay)

    try:
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Stay updated successfully"})
        return JsonResponse({"success": False, "errors": form.errors}, status=400)
    except Exception as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=400)


def delete(request, pk):
    stay = get_object_or_404(Stay, pk=pk)
    stay.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "Stay deleted successfully"})

    messages.success(request, "Stay deleted successfully")
    return redirect("stay_list")


def select(request):
    keyword = request.GET.get("term", "").strip()

    queryset = Stay.objects.select_related("guest", "room").all()
    if keyword:
        filters = Q(guest__name__icontains=keyword) | Q(room__room_number__icontains=keyword)
        if keyword.isdigit():
            filters |= Q(stay_id=int(keyword))
        queryset = queryset.filter(filters)

    queryset = queryset.order_by("-created_at")[:20]
    results = [
        {
            "id": item.stay_id,
            "text": f"Stay #{item.stay_id} - {item.guest.name}",
        }
        for item in queryset
    ]
    return JsonResponse({"results": results})
