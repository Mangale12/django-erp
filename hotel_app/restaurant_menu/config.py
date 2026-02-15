# reception/config.py
from hotel_app.restaurant_menu.views import (
    menu_category_view,
    menu_sub_category_view,
    menu_item_view,
    modifier_view,
    zone_view,
    table_setup_view,
    order_view,
    kitchen_type_view,
    outlet_view,
    kitchen_view
)

from hotel_app.restaurant_menu.datatables.menu_category_data_table import MenuCategoryDataTable
from hotel_app.restaurant_menu.datatables.menu_sub_category_data_table import MenuSubCategoryDataTable
from hotel_app.restaurant_menu.datatables.menu_item_data_table import MenuItemDataTable
from hotel_app.restaurant_menu.datatables.modifier_data_table import ModifierDataTable
from hotel_app.restaurant_menu.datatables.zone_data_table import ZoneDataTable
from hotel_app.restaurant_menu.datatables.table_setup_data_table import TableSetupDataTable
from hotel_app.restaurant_menu.datatables.order_data_table import OrderDataTable
from hotel_app.restaurant_menu.datatables.kitchen_type_data_table import KitchenTypeDataTable
from hotel_app.restaurant_menu.datatables.outlet_data_table import OutletDataTable
from hotel_app.restaurant_menu.datatables.kitchen_data_table import KitchenDataTable

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
    {
        'name': 'menu_item',
        'view_module': menu_item_view,
        'datatable_view': MenuItemDataTable,
        'verbose_name': 'Menu Item'
    },
    {
        'name': 'modifier',
        'view_module': modifier_view,
        'datatable_view': ModifierDataTable,
        'verbose_name': 'Modifier'
    },
    {
        'name': 'zone',
        'view_module': zone_view,
        'datatable_view': ZoneDataTable,
        'verbose_name': 'Zone'
    },
    {
        'name': 'table_setup',
        'view_module': table_setup_view,
        'datatable_view': TableSetupDataTable,
        'verbose_name': 'Table Setup'
    },
    {
        'name': 'order',
        'view_module': order_view,
        'datatable_view': OrderDataTable,
        'verbose_name': 'Order'
    },
    {
        'name': 'kitchen_type',
        'view_module': kitchen_type_view,
        'datatable_view': KitchenTypeDataTable,
        'verbose_name': 'Kitchen Type'
    },
    {
        'name': 'outlet',
        'view_module': outlet_view,
        'datatable_view': OutletDataTable,
        'verbose_name': 'Outlet'
    },
    {
        'name': 'kitchen',
        'view_module': kitchen_view,
        'datatable_view': KitchenDataTable,
        'verbose_name': 'Kitchen'
    }
]