import json
from django.views.decorators.cache import never_cache

def room_type_table_config(request):
    config = {
        'columns': [
            {'data': 'name', 'title': 'Name'},
            {'data': 'code', 'title': 'Code'},
            {'data': 'max_adults', 'title': 'Max Adults', 'className': 'text-center'},
            {'data': 'max_children', 'title': 'Max Children', 'className': 'text-center'},
            {'data': 'default_rate', 'title': 'Default Rate', 'className': 'text-end'},
            {
                'data': 'is_active',
                'title': 'Status',
                'className': 'text-center',
                'render': "function(data, type, row) { return data ? '<span class=\'badge bg-success\'>Active</span>' : '<span class=\'badge bg-danger\'>Inactive</span>'; }"
            },
            {
                'data': 'id',
                'title': 'Actions',
                'orderable': False,
                'className': 'text-center',
                'render': "function(data, type, row) { return '<div class=\'btn-group\' role=\'group\'><button type=\'button\' class=\'btn btn-sm btn-outline-primary edit-room-type\' data-id=\'' + data + '\'><i class=\'fas fa-edit\'></i></button><button type=\'button\' class=\'btn btn-sm btn-outline-danger delete-room-type\' data-id=\'' + data + '\'><i class=\'fas fa-trash\'></i></button></div>'; }"
            }
        ],
        'order': [[0, 'asc']],
        'pageLength': 10,
        'responsive': True,
        'processing': True,
        'serverSide': True,
        'ajax': '/room-types/datatable/'
    }
    
    # Convert to JSON string for template
    return {
        'room_type_table_config': json.dumps(config)
    }
