from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import require_http_methods

from master_setup.models import FiscalYear


def index(request):
    fields = [
        {"name": "fiscal_year_name", "label": "Fiscal Year Name", "type": "text", "required": True},
        {"name": "start_date", "label": "Start Date", "type": "date", "required": True},
        {"name": "end_date", "label": "End Date", "type": "date", "required": True},
        {"name": "description", "label": "Description", "type": "textarea"},
        {"name": "is_active", "label": "Active", "type": "checkbox", "default": True},
    ]
    return render(request, "master_setup/fiscal_year.html", {"fields": fields})


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "POST":
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        try:
            with transaction.atomic():
                fiscal_year = FiscalYear.objects.create(
                    fiscal_year_name=request.POST.get("fiscal_year_name"),
                    start_date=request.POST.get("start_date"),
                    end_date=request.POST.get("end_date"),
                    description=request.POST.get("description"),
                    is_active=bool(request.POST.get("is_active")),
                )

                if is_ajax:
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "Fiscal Year created successfully",
                            "fiscal_year": {
                                "id": fiscal_year.id,
                                "fiscal_year_name": fiscal_year.fiscal_year_name,
                                "start_date": fiscal_year.start_date,
                                "end_date": fiscal_year.end_date,
                                "description": fiscal_year.description,
                                "is_active": fiscal_year.is_active,
                                "edit_url": reverse("fiscal_year_update", args=[fiscal_year.id]),
                                "delete_url": reverse("fiscal_year_delete", args=[fiscal_year.id]),
                            },
                        }
                    )

                messages.success(request, "Fiscal Year created successfully")
                return redirect("fiscal_year_list")

        except Exception as exc:
            if is_ajax:
                return JsonResponse({"success": False, "error": str(exc)}, status=400)
            messages.error(request, f"Error creating fiscal year: {exc}")
            return redirect("fiscal_year_list")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    return render(request, "master_setup/fiscal_year/form.html")


def edit(request, pk):
    fiscal_year = get_object_or_404(FiscalYear, pk=pk)
    return JsonResponse(
        {
            "success": True,
            "data": {
                "id": fiscal_year.id,
                "fiscal_year_name": fiscal_year.fiscal_year_name,
                "start_date": fiscal_year.start_date,
                "end_date": fiscal_year.end_date,
                "description": fiscal_year.description,
                "is_active": fiscal_year.is_active,
            },
        }
    )


def update(request, pk):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

    fiscal_year = get_object_or_404(FiscalYear, pk=pk)

    try:
        fiscal_year.fiscal_year_name = request.POST.get("fiscal_year_name")
        fiscal_year.start_date = request.POST.get("start_date")
        fiscal_year.end_date = request.POST.get("end_date")
        fiscal_year.description = request.POST.get("description", "")
        fiscal_year.is_active = bool(request.POST.get("is_active"))
        fiscal_year.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Fiscal Year updated successfully",
                "fiscal_year": {
                    "id": fiscal_year.id,
                    "fiscal_year_name": fiscal_year.fiscal_year_name,
                    "start_date": fiscal_year.start_date,
                    "end_date": fiscal_year.end_date,
                    "description": fiscal_year.description,
                    "is_active": fiscal_year.is_active,
                    "edit_url": reverse("fiscal_year_update", args=[fiscal_year.id]),
                    "delete_url": reverse("fiscal_year_delete", args=[fiscal_year.id]),
                },
            }
        )
    except Exception as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=400)


def delete(request, pk):
    fiscal_year = get_object_or_404(FiscalYear, pk=pk)
    fiscal_year.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "Fiscal Year deleted successfully"})

    messages.success(request, "Fiscal Year deleted successfully")
    return redirect("fiscal_year_list")


def select(request):
    keyword = request.GET.get("term", "").strip()

    queryset = FiscalYear.objects.all()

    if keyword:
        queryset = queryset.filter(fiscal_year_name__icontains=keyword)

    queryset = queryset.order_by("-created_at")[:5]

    results = [{"id": item.id, "text": item.fiscal_year_name} for item in queryset]

    return JsonResponse({"results": results})
