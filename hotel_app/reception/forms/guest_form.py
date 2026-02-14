from django import forms
from hotel_app.reception.models import Guest
from django.core.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta

class GuestForm(forms.ModelForm):
    # Overriding gender to provide choices
    GENDER_CHOICES = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other'),
    ]

    ID_PROOF_TYPE_CHOICES = [
        ('a', 'Aadhar'),
        ('p', 'Passport'),
        ('v', 'Voter ID'),
        ('l', 'License'),
        ('s', 'Student ID'),
        ('c', 'Citizenship'),
    ]
    
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    id_proof_type = forms.ChoiceField(choices=ID_PROOF_TYPE_CHOICES, required=True)

    class Meta:
        model = Guest
        fields = [
            'name', 'gender', 'dob', 'country', 'nationality', 
            'id_proof_type', 'id_proof_number', 'phone',    
            'email', 'address', 'state', 'city', 'guest_type', 'remarks'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Making specific fields required at the form level
        required_fields = [
            'name', 'country', 'nationality', 'id_proof_type', 
            'id_proof_number', 'phone', 'email', 'address'
        ]
        for field in required_fields:
            self.fields[field].required = True

    def clean_dob(self):
        """Validation: DOB must be at least 18 years before today"""
        dob = self.cleaned_data.get('dob')
        if dob:
            eighteen_years_ago = date.today() - relativedelta(years=18)
            if dob > eighteen_years_ago:
                raise ValidationError("Guest must be at least 18 years old.")
        return dob

    def clean_email(self):
        """Basic email format validation"""
        email = self.cleaned_data.get('email')
        if email and "@" not in email:
            raise ValidationError("Please enter a valid email address.")
        return email