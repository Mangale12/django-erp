from django import forms
from django.core.exceptions import ValidationError
from hotel_app.rooms.models import RoomAllotment

class RoomAllotmentForm(forms.ModelForm):

    class Meta:
        model = RoomAllotment
        fields = [
            'booking',
            'room',
            'alloted_by',
            # 'alloted_at'
        ]

   

    
