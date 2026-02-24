from django import forms
from django.forms import inlineformset_factory
from ..models import BillMaster, BillLineItem

class BillMasterForm(forms.ModelForm):
    class Meta:
        model = BillMaster
        # Exclude auto-calculated fields from manual user input to prevent errors
        exclude = ['bill_no', 'grand_total', 'tax_amount', 'discount_amount', 'created_by']
        widgets = {
            'bill_status': forms.Select(attrs={'class': 'form-select'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Custom Validation: Ensure a bill has either a Guest or a Room if it's not a walk-in
        guest = cleaned_data.get("guest")
        room = cleaned_data.get("room")
        if not guest and not room:
            raise forms.ValidationError("A bill must be associated with at least a Guest or a Room.")
        return cleaned_data

class BillLineItemForm(forms.ModelForm):
    class Meta:
        model = BillLineItem
        fields = ['item', 'quantity', 'rate', 'is_complementary']

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty is None:
            return qty
        if qty <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return qty

# This creates a bridge between Master and Line Items
BillLineItemFormSet = inlineformset_factory(
    BillMaster, 
    BillLineItem, 
    form=BillLineItemForm,
    extra=1, # Number of empty rows to show
    can_delete=True
)
