# user_management/config.py
from user_management.views import (
    user_view,
)

from .datatables.user_data_table import UserDataTable
from django.contrib.auth.models import User

# Define all your CRUD entities in one place
USER_ENTITIES = [
    {
        'name': 'user',
        'view_module': user_view,
        'datatable_view': UserDataTable,
        'verbose_name': 'User'
    },
]