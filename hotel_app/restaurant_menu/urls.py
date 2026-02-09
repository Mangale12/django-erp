# reception/urls.py
from django.urls import path
from .config import RESTAURANT_ENTITIES

urlpatterns = []

for entity in RESTAURANT_ENTITIES:
    name = entity['name']
    views = entity['view_module']
    
    urlpatterns.extend([
        path(f'{name}/', views.index, name=f'{name}_list'),
        path(f'{name}/create/', views.create, name=f'{name}_create'),
        path(f'{name}/<int:pk>/update/', views.update, name=f'{name}_update'),
        path(f'{name}/<int:pk>/edit/', views.edit, name=f'{name}_edit'),
        path(f'{name}/delete/<int:pk>/', views.delete, name=f'{name}_delete'),
        
        # AJAX endpoints (if needed)
        path(f'{name}/update_ajax/<int:pk>/', views.edit, name=f'{name}_update_ajax'),
        path(f'{name}/edit_ajax/<int:pk>/', views.edit, name=f'{name}_edit_ajax'),

        path(f"{name}/datatable/", entity['datatable_view'].as_view(), name=f"{name}_datatable"),
        path(f"{name}/select/", views.select, name=f"{name}_select"),
    ])