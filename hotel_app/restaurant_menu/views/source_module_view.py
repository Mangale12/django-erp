from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from hotel_app.restaurant_menu.models import SourceModule


def _build_fields():
    return [
        {"name": "module_name", "label": "Module Name", "type": "text", "required": True},
        {"name": "module_code", "label": "Module Code", "type": "text", "required": True},
        {
            "name": "is_postable_to_folio",
            "label": "Is Postable To Folio",
            "type": "checkbox",
            "default": False,
        },
        {"name": "is_active", "label": "Is Active", "type": "checkbox", "default": True},
    ]


def _save_source_module_from_post(source_module_obj, post_data):
    source_module_obj.module_name = (post_data.get("module_name") or "").strip()
    source_module_obj.module_code = (post_data.get("module_code") or "").strip().upper()
    source_module_obj.is_postable_to_folio = bool(post_data.get("is_postable_to_folio"))
    source_module_obj.is_active = bool(post_data.get("is_active"))
    source_module_obj.save()
    return source_module_obj


@login_required
def index(request):
    return render(request, "restaurant_menu/source_module/list.html", {"fields": _build_fields()})


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "GET":
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Invalid request method"}, status=405)
        return redirect("source_module_list")

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    try:
        with transaction.atomic():
            _save_source_module_from_post(SourceModule(), request.POST)
        if is_ajax:
            return JsonResponse({"success": True, "message": "Source module created successfully"})
        messages.success(request, "Source module created successfully")
        return redirect("source_module_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error creating source module: {exc}")
        return redirect("source_module_list")


@login_required
@require_http_methods(["POST"])
def update(request, pk):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    source_module_obj = get_object_or_404(SourceModule, pk=pk)
    try:
        with transaction.atomic():
            _save_source_module_from_post(source_module_obj, request.POST)
        if is_ajax:
            return JsonResponse({"success": True, "message": "Source module updated successfully"})
        messages.success(request, "Source module updated successfully")
        return redirect("source_module_list")
    except Exception as exc:
        if is_ajax:
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        messages.error(request, f"Error updating source module: {exc}")
        return redirect("source_module_list")


@login_required
def edit(request, pk):
    source_module_obj = get_object_or_404(SourceModule, pk=pk)
    payload = {
        "id": source_module_obj.pk,
        "module_name": source_module_obj.module_name,
        "module_code": source_module_obj.module_code,
        "is_postable_to_folio": source_module_obj.is_postable_to_folio,
        "is_active": source_module_obj.is_active,
    }
    return JsonResponse({"success": True, "data": payload, **payload})


@login_required
@require_http_methods(["POST"])
def delete(request, pk):
    source_module_obj = get_object_or_404(SourceModule, pk=pk)
    source_module_obj.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "Source module deleted successfully"})

    messages.success(request, "Source module deleted successfully")
    return redirect("source_module_list")


@login_required
def select(request):
    keyword = (request.GET.get("term") or request.GET.get("q") or "").strip()

    queryset = SourceModule.objects.all()
    if keyword:
        queryset = queryset.filter(Q(module_name__icontains=keyword) | Q(module_code__icontains=keyword))

    queryset = queryset.order_by("module_name")[:20]
    results = [{"id": item.pk, "text": f"{item.module_name} ({item.module_code})"} for item in queryset]
    return JsonResponse({"results": results})
