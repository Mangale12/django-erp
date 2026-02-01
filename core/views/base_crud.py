from django.http import JsonResponse
from django.shortcuts import get_object_or_404

class BaseAjaxCRUD:
    model = None
    form_class = None

    def create_or_update(self, request, pk=None):
        instance = self.model.objects.filter(pk=pk).first()
        form = self.form_class(request.POST, instance=instance)

        if form.is_valid():
            obj = form.save()
            return JsonResponse({"success": True, "id": obj.id})

        return JsonResponse({"error": form.errors}, status=400)

    def retrieve(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return JsonResponse({
            field.name: getattr(obj, field.name)
            for field in obj._meta.fields
        })

    def delete(self, request, pk):
        get_object_or_404(self.model, pk=pk).delete()
        return JsonResponse({"success": True})
