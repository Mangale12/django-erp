from django.urls import path
from hotel_app.rooms.datatables.RoomTypeDataTable import RoomTypeDataTable
from hotel_app.rooms.datatables.RoomCategoryDataTable import RoomCategoryDataTable
from hotel_app.rooms.datatables.room_view_type_data_table import RoomViewTypeDataTable
from hotel_app.rooms.datatables.room_amnity_data_table import RoomAmnityDataTable
from hotel_app.rooms.datatables.room_status_data_table import RoomStatusDataTable
from hotel_app.rooms.datatables.bed_type_data_table import BedTypeDataTable
from hotel_app.rooms.datatables.block_data_table import BlockDataTable
from hotel_app.rooms.datatables.floor_data_table import FloorDataTable
from hotel_app.rooms.datatables import RoomDataTable
from hotel_app.rooms.datatables import RoomRateDataTable
from hotel_app.rooms.datatables import RoomAllotmentDataTable


from hotel_app.rooms.views.room_type import (
    room_type_list,
    room_type_create,
    room_type_edit,
    room_type_delete,
    room_type_update_ajax,
    room_type_select,
)
from hotel_app.rooms.views.room_category import (
    room_category_list,
    room_category_create,
    room_category_update,
    room_category_delete,
    room_category_json,
    room_category_update_ajax,
    room_category_edit,
    room_category_select,
)
from hotel_app.rooms.views.room_view_type import (
    room_view_type_list,
    room_view_type_create,
    room_view_type_edit,
    room_view_type_delete,
    room_view_type_update_ajax,
    room_view_type_update,
    room_view_type_select,
)
from hotel_app.rooms.views.room_amnity import (
    room_amnity_list,
    room_amnity_create,
    room_amnity_update,
    room_amnity_delete,
    room_amnity_json,
    room_amnity_update_ajax,
    room_amnity_edit,
    room_amnity_select,
)
from hotel_app.rooms.views.room_status import (
    room_status_list,
    room_status_create,
    room_status_update,
    room_status_edit,
    room_status_delete,
    room_status_update_ajax,
    room_status_select,
)

from hotel_app.rooms.views.bed_type import (
    bed_type_list,
    bed_type_create,
    bed_type_update,
    bed_type_delete,
    bed_type_update_ajax,
    bed_type_edit,
    bed_type_select,
)

from hotel_app.rooms.views.block import (
    block_list,
    block_create,
    block_update,
    block_delete,
    block_update_ajax,
    block_edit,
    block_select,
)

from hotel_app.rooms.views.floor import (
    floor_list,
    floor_create,
    floor_update,
    floor_delete,
    floor_update_ajax,
    floor_edit,
    floor_select,
)

from hotel_app.rooms.views.room_view import (
    room_list,
    room_create,
    room_edit,
    room_delete,
    room_update_ajax,
    room_update,
    room_edit,
    room_select,
    
)

from hotel_app.rooms.views.room_rate_view import (
    room_rate_list,
    room_rate_create,
    room_rate_update,
    room_rate_delete,
    room_rate_edit,
    room_rate_select,
)

from hotel_app.rooms.views.room_allotment_view import (
    room_allotment_list,
    room_allotment_create,
    room_allotment_update,
    room_allotment_delete,
    room_allotment_edit,
    room_allotment_select,
    room_allotment_view,
)

urlpatterns = [
    path('room-types/', room_type_list, name='room_type_list'),
    path('room-types/create/', room_type_create, name='room_type_create'),
    path('room-types/<int:pk>/update/', room_type_update_ajax, name='room_type_update'),
    path('room-types/<int:pk>/edit/', room_type_edit, name='room_type_edit'),
    path('room-types/<int:pk>/delete/', room_type_delete, name='room_type_delete'),
    path("room-types/datatable/", RoomTypeDataTable.as_view(), name="room_type_datatable"),
    path('room-types/select/', room_type_select, name='room_type_select'),

    path('room-categories/', room_category_list, name='room_category_list'),
    path('room-categories/create/', room_category_create, name='room_category_create'),
    path('room-categories/<int:pk>/', room_category_json, name='room_category_json'),
    path('room-categories/<int:pk>/update/', room_category_update_ajax, name='room_category_update'),
    path('room-categories/<int:pk>/edit/', room_category_edit, name='room_category_edit'),
    path('room-categories/<int:pk>/delete/', room_category_delete, name='room_category_delete'),
    path("room-categories/datatable/", RoomCategoryDataTable.as_view(), name="room_category_datatable"),
    path('room-categories/select/', room_category_select, name='room_category_select'),

    path('room/', room_list, name='room_list'),
    path('room/create/', room_create, name='room_create'),
    path('room/<int:pk>/update/', room_update_ajax, name='room_update_ajax'),
    path('room/<int:pk>/edit/', room_edit, name='room_edit'),
    path('room/<int:pk>/', room_update, name='room_update'),
    path('room/<int:pk>/delete/', room_delete, name='room_delete'),
    path("room/datatable/", RoomDataTable.as_view(), name="room_datatable"),
    path('room/select/', room_select, name='room_select'),

    path('room-view-type/', room_view_type_list, name='room_view_type_list'),
    path('room-view-type/create/', room_view_type_create, name='room_view_type_create'),
    path('room-view-type/<int:pk>/update/', room_view_type_update_ajax, name='room_view_type_update'),
    path('room-view-type/<int:pk>/edit/', room_view_type_edit, name='room_view_type_edit'),
    path('room-view-type/<int:pk>/', room_view_type_update, name='room_view_type_update'),
    path('room-view-type/<int:pk>/delete/', room_view_type_delete, name='room_view_type_delete'),
    path("room-view-type/datatable/", RoomViewTypeDataTable.as_view(), name="room_view_type_datatable"),
    path('room-view-type/select/', room_view_type_select, name='room_view_type_select'),

    path('room-amnities/', room_amnity_list, name='room_amnity_list'),
    path('room-amnities/create/', room_amnity_create, name='room_amnity_create'),
    path('room-amnities/<int:pk>/update/', room_amnity_update_ajax, name='room_amnity_update'),
    path('room-amnities/<int:pk>/edit/', room_amnity_edit, name='room_amnity_edit'),
    path('room-amnities/<int:pk>/', room_amnity_update, name='room_amnity_update'),
    path('room-amnities/<int:pk>/delete/', room_amnity_delete, name='room_amnity_delete'),
    path("room-amnities/datatable/", RoomAmnityDataTable.as_view(), name="room_amnity_datatable"),
    path('room-amnities/select/', room_amnity_select, name='room_amnity_select'),

    path('room-status/', room_status_list, name='room_status_list'),
    path('room-status/create/', room_status_create, name='room_status_create'),
    path('room-status/<int:pk>/update/', room_status_update_ajax, name='room_status_update'),
    path('room-status/<int:pk>/edit/', room_status_edit, name='room_status_edit'),
    path('room-status/<int:pk>/', room_status_update, name='room_status_update'),
    path('room-status/<int:pk>/delete/', room_status_delete, name='room_status_delete'),
    path("room-status/datatable/", RoomStatusDataTable.as_view(), name="room_status_datatable"),
    path('room-status/select/', room_status_select, name='room_status_select'),

    path('bed-types/', bed_type_list, name='bed_type_list'),
    path('bed-types/create/', bed_type_create, name='bed_type_create'),
    path('bed-types/<int:pk>/update/', bed_type_update_ajax, name='bed_type_update'),
    path('bed-types/<int:pk>/edit/', bed_type_edit, name='bed_type_edit'),
    path('bed-types/<int:pk>/', bed_type_update, name='bed_type_update'),
    path('bed-types/<int:pk>/delete/', bed_type_delete, name='bed_type_delete'),
    path("bed-types/datatable/", BedTypeDataTable.as_view(), name="bed_type_datatable"),
    path('bed-types/select/', bed_type_select, name='bed_type_select'),

    path('blocks/', block_list, name='block_list'),
    path('blocks/create/', block_create, name='block_create'),
    path('blocks/<int:pk>/update/', block_update_ajax, name='block_update'),
    path('blocks/<int:pk>/edit/', block_edit, name='block_edit'),
    path('blocks/<int:pk>/', block_update, name='block_update'),
    path('blocks/<int:pk>/delete/', block_delete, name='block_delete'),
    path("blocks/datatable/", BlockDataTable.as_view(), name="block_datatable"),
    path('blocks/select/', block_select, name='block_select'),

    path('floors/', floor_list, name='floor_list'),
    path('floors/create/', floor_create, name='floor_create'),
    path('floors/<int:pk>/update/', floor_update_ajax, name='floor_update'),
    path('floors/<int:pk>/edit/', floor_edit, name='floor_edit'),
    path('floors/<int:pk>/', floor_update, name='floor_update'),
    path('floors/<int:pk>/delete/', floor_delete, name='floor_delete'),
    path("floors/datatable/", FloorDataTable.as_view(), name="floor_datatable"),
    path('floors/select/', floor_select, name='floor_select'),

    path('room-rates/', room_rate_list, name='room_rate_list'),
    path('room-rates/create/', room_rate_create, name='room_rate_create'),
    path('room-rates/<int:pk>/edit/', room_rate_edit, name='room_rate_edit'),
    path('room-rates/<int:pk>/', room_rate_update, name='room_rate_update'),
    path('room-rates/<int:pk>/delete/', room_rate_delete, name='room_rate_delete'),
    path("room-rates/datatable/", RoomRateDataTable.as_view(), name="room_rate_datatable"),
    path('room-rates/select/', room_rate_select, name='room_rate_select'),

    path('room-allotments/', room_allotment_list, name='room_allotment_list'),
    path('room-allotments/create/', room_allotment_create, name='room_allotment_create'),
    path('room-allotments/<int:pk>/edit/', room_allotment_edit, name='room_allotment_edit'),
    path('room-allotments/<int:pk>/', room_allotment_update, name='room_allotment_update'),
    path('room-allotments/<int:pk>/delete/', room_allotment_delete, name='room_allotment_delete'),
    path("room-allotments/datatable/", RoomAllotmentDataTable.as_view(), name="room_allotment_datatable"),
    path('room-allotments/select/', room_allotment_select, name='room_allotment_select'),
    path('room-allotments/view/<int:pk>/', room_allotment_view, name='room_allotment_view'),
]