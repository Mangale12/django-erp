from django import forms
from hotel_app.restaurant_menu.models import Order, OrderItem, OrderItemModifier
from hotel_app.rooms.models import Room
from hotel_app.restaurant_menu.models import TableSetup

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['table'].queryset = TableSetup.objects.filter(is_active=True)
        self.fields['room'].queryset = Room.objects.filter(is_active=True)
        