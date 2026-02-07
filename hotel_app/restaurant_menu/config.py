# reception/config.py
from hotel_app.restaurant_menu.views import (
    menu_category_view,
    menu_sub_category_view
)

from hotel_app.restaurant_menu.datatables.menu_category_data_table import MenuCategoryDataTable
from hotel_app.restaurant_menu.datatables.menu_sub_category_data_table import MenuSubCategoryDataTable


# Define all your CRUD entities in one place
RESTAURANT_ENTITIES = [
    {
        'name': 'menu_category',
        'view_module': menu_category_view,
        'datatable_view': MenuCategoryDataTable,
        'verbose_name': 'Menu Category'
    },
    {
        'name': 'menu_sub_category',
        'view_module': menu_sub_category_view,
        'datatable_view': MenuSubCategoryDataTable,
        'verbose_name': 'Menu Sub Category'
    },
]