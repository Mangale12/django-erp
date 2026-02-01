import django.db.models as models


class Guest(models.Model):
    name = models.CharField(max_length=256, unique=False, null=True, blank=True, help_text='Name of the guest (max 256 characters)')
    gender = models.CharField(max_length=256, unique=False, null=True, blank=True, help_text='Gender of the guest (max 256 characters)')
    dob = models.DateField(unique=False, null=True, blank=True, help_text='Date of birth of the guest (max 256 characters)')
    age = models.IntegerField(unique=False, null=True, blank=True, help_text='Age of the guest (max 256 characters)')
    country = models.ForeignKey('master_setup.Country', null=True, blank=True, on_delete=models.CASCADE, related_name='guests')
    state = models.CharField(max_length=256, unique=False, null=True, blank=True, help_text='State of the guest (max 256 characters)')
    city = models.CharField(max_length=256, unique=False, null=True, blank=True, help_text='City of the guest (max 256 characters)')

    nationality = models.CharField(max_length=256, unique=False, null=True, blank=True, help_text='Nationality of the guest (max 256 characters)')
    id_proof_type = models.CharField(max_length=256, unique=False, null=True, blank=True, help_text='ID proof type of the guest (max 256 characters)')
    id_proof_number = models.CharField(max_length=256, unique=False, null=True, blank=True, help_text='ID proof number of the guest (max 256 characters)')
    phone = models.CharField(max_length=256, unique=False, null=True, blank=True, help_text='Mobile number of the guest (max 256 characters)')
    email = models.CharField(max_length=256, unique=False, null=True, blank=True, help_text='Email of the guest (max 256 characters)')
    address = models.CharField(max_length=256, unique=False, null=True, blank=True, help_text='Address of the guest (max 256 characters)')
    guest_type = models.CharField(max_length=256, unique=False, null=True, blank=True, help_text='Guest type of the guest (max 256 characters)')
    remarks = models.TextField(unique=False, null=True, blank=True, help_text='Remarks of the guest (max 256 characters)')
    is_active = models.BooleanField(default=True, help_text='Is the guest active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the guest was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the guest was last updated')
    
    def __str__(self):
        return self.name
        