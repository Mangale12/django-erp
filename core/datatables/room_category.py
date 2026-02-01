from .base import BaseDataTable
from rooms.models import RoomCategory

class RoomCategoryDataTable(BaseDataTable):
    model = RoomCategory
    columns = ["name", "code", "is_active"]
    search_fields = ["name", "code"]

    def render_column(self, obj, column):
        if column == "is_active":
            return "Yes" if obj.is_active else "No"
        return super().render_column(obj, column)
