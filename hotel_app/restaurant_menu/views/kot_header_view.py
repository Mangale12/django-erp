# hotel_app/restaurant_menu/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count
from ..models import KOTHeader
from ..forms import KOTHeaderForm
from hotel_app.restaurant_menu.models import KOTStatus
from django.urls import reverse
from django.http import JsonResponse


@login_required
def index(request):
    fields = [
        {"name": "kot_number", "label": "KOT Number", "type": "text", "required": True},
        {"name": "business_date", "label": "Business Date", "type": "date", "required": True},
        {"name": "outlet", "label": "Outlet", "type": "select", "required": True, "url" : reverse('outlet_select')},
        {"name": "shift_type", "label": "Shift Type", "type": "select", "required": True, "url" : reverse('shift_type_select')},
        {"name": "order", "label": "Order", "type": "select", "required": True, "url" : reverse('order_select')},
        {"name": "table", "label": "Table", "type": "select", "required": True, "url" : reverse('table_setup_select')},
        {"name": "room", "label": "Room", "type": "select", "required": True, "url" : reverse('room_select')},
        {"name": "guest", "label": "Guest", "type": "select", "required": True, "url" : reverse('guest_select')},
        {"name": "kitchen", "label": "Kitchen", "type": "select", "required": True, "url" : reverse('kitchen_select')},
        {"name": "cover_count", "label": "Cover Count", "type": "number", "required": True},
        {"name": "kot_type", "label": "KOT Type", "type": "select", "required": True, "url" : reverse('kot_type_select')},
        {"name": "kot_status", "label": "KOT Status", "type": "select", "required": True, "url" : reverse('kot_status_select')},
        {"name": "priority_level", "label": "Priority Level", "type": "select", "required": True, "url" : reverse('priority_level_select')},
        {"name": "is_urgent", "label": "Is Urgent", "type": "checkbox", "required": False},
        {"name": "is_reprint", "label": "Is Reprint", "type": "checkbox", "required": False},
        {"name": "reprint_count", "label": "Reprint Count", "type": "number", "required": False},
        {"name": "printed_at", "label": "Printed At", "type": "datetime", "required": True},
        {"name": "completed_at", "label": "Completed At", "type": "datetime", "required": True},
        {"name": "total_item_count", "label": "Total Item Count", "type": "number", "required": True},
        {"name": "total_quantity", "label": "Total Quantity", "type": "number", "required": True},
        {"name": "is_stock_posted", "label": "Is Stock Posted", "type": "checkbox", "required": False},
        {"name": "stock_posted_at", "label": "Stock Posted At", "type": "datetime", "required": True},
        {"name": "transfer_from_kitchen", "label": "Transfer From Kitchen", "type": "select", "required": True, "url" : reverse('kitchen_select')},
        {"name": "transfer_to_kitchen", "label": "Transfer To Kitchen", "type": "select", "required": True, "url" : reverse('kitchen_select')},
        {"name": "transfer_at", "label": "Transfer At", "type": "datetime", "required": True},
        {"name": "cancelled_at", "label": "Cancelled At", "type": "datetime", "required": True},
        {"name": "cancellation_reason", "label": "Cancellation Reason", "type": "text", "required": True},
    ]
    return render(request, 'restaurant_menu/kot_header/list.html', {'fields': fields})


@login_required
def create(request):
    """Create new KOT Header"""
    if request.method == 'POST':
        form = KOTHeaderForm(request.POST)
        if form.is_valid():
            kot_header = form.save(commit=False)
            kot_header.created_by = request.user
            kot_header.create_at = timezone.now()
            
            # Auto-generate KOT number if not provided
            if not kot_header.kot_number:
                last_kot = KOTHeader.objects.filter(
                    business_date=timezone.now().date()
                ).order_by('-id').first()
                if last_kot and last_kot.kot_number:
                    try:
                        last_number = int(last_kot.kot_number.split('-')[-1])
                        kot_number = f"KOT-{timezone.now().strftime('%Y%m%d')}-{last_number + 1:04d}"
                    except:
                        kot_number = f"KOT-{timezone.now().strftime('%Y%m%d')}-0001"
                else:
                    kot_number = f"KOT-{timezone.now().strftime('%Y%m%d')}-0001"
                kot_header.kot_number = kot_number
            
            kot_header.save()
            return JsonResponse({
                'success': True,
                'message': 'KOT Type updated successfully',
            })
            
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = KOTHeaderForm()
    
    context = {
        'form': form,
        'page_title': 'Create KOT Header',
        'page_subtitle': 'Kitchen Order Ticket',
    }
    return render(request, 'restaurant_menu/kot_header_form.html', context)


@login_required
def update(request, pk):
    """Update existing KOT Header"""
    kot_header = get_object_or_404(KOTHeader, pk=pk)
    
    if request.method == 'POST':
        form = KOTHeaderForm(request.POST, instance=kot_header)
        if form.is_valid():
            kot_header = form.save(commit=False)
            
            # Handle status change to completed
            if kot_header.kot_status and kot_header.kot_status.status_name == 'Completed':
                if not kot_header.completed_at:
                    kot_header.completed_at = timezone.now()
            
            # Handle cancellation
            if kot_header.kot_status and kot_header.kot_status.status_name == 'Cancelled':
                if not kot_header.cancelled_by:
                    kot_header.cancelled_by = request.user
                    kot_header.cancelled_at = timezone.now()
            
            kot_header.save()
            messages.success(request, f'KOT {kot_header.kot_number} updated successfully!')
            return redirect('restaurant_menu:kot_header_detail', pk=kot_header.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = KOTHeaderForm(instance=kot_header)
    
    context = {
        'form': form,
        'kot_header': kot_header,
        'page_title': 'Update KOT Header',
        'page_subtitle': f'KOT {kot_header.kot_number}',
    }
    return render(request, 'restaurant_menu/kot_header_form.html', context)





@login_required
def detail(request, pk):
    """View KOT Header details"""
    kot_header = get_object_or_404(
        KOTHeader.objects.select_related(
            'outlet', 'kitchen', 'waiter', 'captain', 'kot_type', 'kot_status',
            'order', 'table', 'room', 'guest'
        ),
        pk=pk
    )
    
    context = {
        'kot_header': kot_header,
        'page_title': 'KOT Details',
        'page_subtitle': f'KOT {kot_header.kot_number}',
    }
    return render(request, 'restaurant_menu/kot_header_detail.html', context)

def edit(request, pk):
    """Edit KOT Header"""
    kot_header = get_object_or_404(KOTHeader, pk=pk)
    
    if request.method == 'POST':
        form = KOTHeaderForm(request.POST, instance=kot_header)
        if form.is_valid():
            kot_header = form.save(commit=False)
            
            # Handle completion
            if kot_header.kot_status and kot_header.kot_status.status_name == 'Completed':
                if not kot_header.completed_at:
                    kot_header.completed_at = timezone.now()
            
            # Handle cancellation
            if kot_header.kot_status and kot_header.kot_status.status_name == 'Cancelled':
                if not kot_header.cancelled_by:
                    kot_header.cancelled_by = request.user
                    kot_header.cancelled_at = timezone.now()
            
            kot_header.save()
            messages.success(request, f'KOT {kot_header.kot_number} updated successfully!')
            return redirect('restaurant_menu:kot_header_detail', pk=kot_header.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = KOTHeaderForm(instance=kot_header)
    
    context = {
        'form': form,
        'kot_header': kot_header,
        'page_title': 'Update KOT Header',
        'page_subtitle': f'KOT {kot_header.kot_number}',
    }
    return render(request, 'restaurant_menu/kot_header_form.html', context)

@login_required
def delete(request, pk):
    """Delete KOT Header"""
    kot_header = get_object_or_404(KOTHeader, pk=pk)
    
    if request.method == 'POST':
        kot_number = kot_header.kot_number
        kot_header.delete()
        messages.success(request, f'KOT {kot_number} deleted successfully!')
        return redirect('restaurant_menu:kot_header_list')
    
    context = {
        'kot_header': kot_header,
        'page_title': 'Delete KOT',
        'page_subtitle': f'KOT {kot_header.kot_number}',
    }
    return render(request, 'restaurant_menu/kot_header_confirm_delete.html', context)

def select(request):
    keyword = request.GET.get('term', '').strip()  # Select2 uses `term`

    qs = KOTHeader.objects.all()

    if keyword:
        qs = qs.filter(kot_number__icontains=keyword)


    results = [
        {
            "id": item.id,
            "text": item.kot_number
        }
        for item in qs
    ]

    return JsonResponse({
        "results": results
    })