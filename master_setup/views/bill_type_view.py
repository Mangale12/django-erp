from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import require_http_methods

from master_setup.models import BillType


def index(request):
    fields = [
        {"name": "bill_type_name", "label": "Bill Type Name", "type": "text", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True},
    ]
    return render(request, "master_setup/bill_type.html", {"fields": fields})


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "POST":
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        try:
            with transaction.atomic():
                bill_type = BillType.objects.create(
                    bill_type_name=request.POST.get("bill_type_name"),
                    description=request.POST.get("description"),
                    is_active=bool(request.POST.get("is_active")),
                )

                if is_ajax:
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "Bill Type created successfully",
                            "bill_type": {
                                "id": bill_type.id,
                                "bill_type_name": bill_type.bill_type_name,
                                "description": bill_type.description,
                                "is_active": bill_type.is_active,
                                "edit_url": reverse("bill_type_update", args=[bill_type.id]),
                                "delete_url": reverse("bill_type_delete", args=[bill_type.id]),
                            },
                        }
                    )

                messages.success(request, "Bill Type created successfully")
                return redirect("bill_type_list")

        except Exception as exc:
            if is_ajax:
                return JsonResponse({"success": False, "error": str(exc)}, status=400)
            messages.error(request, f"Error creating bill type: {exc}")
            return redirect("bill_type_list")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    return render(request, "master_setup/bill_type/form.html")


def edit(request, pk):
    bill_type = get_object_or_404(BillType, pk=pk)
    return JsonResponse(
        {
            "success": True,
            "data": {
                "id": bill_type.id,
                "bill_type_name": bill_type.bill_type_name,
                "description": bill_type.description,
                "is_active": bill_type.is_active,
            },
        }
    )


def update(request, pk):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

    bill_type = get_object_or_404(BillType, pk=pk)

    try:
        bill_type.bill_type_name = request.POST.get("bill_type_name")
        bill_type.description = request.POST.get("description", "")
        bill_type.is_active = bool(request.POST.get("is_active"))
        bill_type.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Bill Type updated successfully",
                "bill_type": {
                    "id": bill_type.id,
                    "bill_type_name": bill_type.bill_type_name,
                    "description": bill_type.description,
                    "is_active": bill_type.is_active,
                    "edit_url": reverse("bill_type_update", args=[bill_type.id]),
                    "delete_url": reverse("bill_type_delete", args=[bill_type.id]),
                },
            }
        )
    except Exception as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=400)


def delete(request, pk):
    bill_type = get_object_or_404(BillType, pk=pk)
    bill_type.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "Bill Type deleted successfully"})

    messages.success(request, "Bill Type deleted successfully")
    return redirect("bill_type_list")


def select(request):
    keyword = request.GET.get("term", "").strip()

    queryset = BillType.objects.all()

    if keyword:
        queryset = queryset.filter(bill_type_name__icontains=keyword)

    queryset = queryset.order_by("-created_at")[:5]

    results = [{"id": item.id, "text": item.bill_type_name} for item in queryset]

    return JsonResponse({"results": results})
