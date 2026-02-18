# hotel_app/restaurant_menu/forms.py
from django import forms
from django.utils import timezone
from ..models import KOTHeader
from hotel_app.restaurant_menu.models import KOTStatus, Kitchen
from hotel_app.reception.models import Guest
from hotel_app.rooms.models import Room
from master_setup.models import ShiftType, PriorityLevel
from django.contrib.auth.models import User


class KOTHeaderForm(forms.ModelForm):
    class Meta:
        model = KOTHeader
        fields = [
            'business_date', 'outlet', 'shift_type', 'order', 'table', 'room',
            'guest', 'kot_number', 'kitchen', 'waiter', 'captain', 'cover_count',
            'kot_type', 'kot_status', 'priority_level', 'is_urgent', 'cover_count',
            'total_item_count', 'total_quantity'
        ]
        widgets = {
            'business_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select business date'
            }),
            'outlet': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'shift_type': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'order': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'table': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'room': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'guest': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'kot_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter KOT number',
                'readonly': True  # Auto-generated
            }),
            'kitchen': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'waiter': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'captain': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'cover_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter cover count',
                'min': 1
            }),
            'kot_type': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'kot_status': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'priority_level': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'is_urgent': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'total_item_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Total items',
                'readonly': True  # Auto-calculated
            }),
            'total_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Total quantity',
                'readonly': True  # Auto-calculated
            }),
        }
        labels = {
            'business_date': 'Business Date',
            'outlet': 'Outlet',
            'shift_type': 'Shift Type',
            'order': 'Order',
            'table': 'Table',
            'room': 'Room',
            'guest': 'Guest',
            'kot_number': 'KOT Number',
            'kitchen': 'Kitchen',
            'waiter': 'Waiter',
            'captain': 'Captain',
            'cover_count': 'Cover Count',
            'kot_type': 'KOT Type',
            'kot_status': 'KOT Status',
            'priority_level': 'Priority Level',
            'is_urgent': 'Urgent',
            'total_item_count': 'Total Items',
            'total_quantity': 'Total Quantity',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter queryset for better performance
        if self.instance.pk:
            # Edit mode - keep existing values
            pass
        else:
            # Create mode - set initial values
            self.fields['business_date'].initial = timezone.now().date()
            self.fields['kot_status'].initial = KOTStatus.objects.filter(
                name='Pending'
            ).first()
        
        # Add required attribute to essential fields
        required_fields = ['outlet', 'kitchen', 'kot_type', 'kot_status']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
        
        # Filter users to only show waiters and captains (if you have groups)
        self.fields['waiter'].queryset = User.objects.filter(
            is_active=True
        ).order_by('username')
        self.fields['captain'].queryset = User.objects.filter(
            is_active=True
        ).order_by('username')


class KOTHeaderUpdateForm(KOTHeaderForm):
    """Form for updating existing KOT headers"""
    class Meta(KOTHeaderForm.Meta):
        fields = KOTHeaderForm.Meta.fields + [
            'kot_status', 'priority_level', 'is_urgent', 'cancelation_reason'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make kot_number readonly in update form
        self.fields['kot_number'].widget.attrs['readonly'] = True
