from django.views import View
from rooms.models import RoomCategory
from rooms.forms import RoomCategoryForm
from core.views.base_crud import BaseAjaxCRUD
from core.datatables.room_category import RoomCategoryDataTable

class RoomCategoryCRUD(View, BaseAjaxCRUD):
    model = RoomCategory
    form_class = RoomCategoryForm

    def post(self, request, pk=None):
        return self.create_or_update(request, pk)

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        return RoomCategoryDataTable(request).get_response()

    def delete(self, request, pk):
        return self.delete(request, pk)
