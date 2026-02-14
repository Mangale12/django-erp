import django.db.models as models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True, help_text='Phone number (max 15 characters)')
    employee_code = models.CharField(max_length=15, unique=True, null=True, blank=True, help_text='Employee code (max 15 characters)')
    department  = models.ForeignKey('master_setup.Department', null=True, blank=True, on_delete=models.CASCADE, related_name='users')
    designation  = models.ForeignKey('master_setup.Designation', null=True, blank=True, on_delete=models.CASCADE, related_name='users')
    employee_type = models.ForeignKey('master_setup.EmployeeType', null=True, blank=True, on_delete=models.CASCADE, related_name='users')
    probation_end_date = models.DateField(null=True, blank=True, help_text='Probation end date')
    salary_structure = models.ForeignKey('master_setup.SalaryStructure', null=True, blank=True, on_delete=models.CASCADE, related_name='users')
    payment_mode = models.ForeignKey('master_setup.PaymentMode', null=True, blank=True, on_delete=models.CASCADE, related_name='users')
    country = models.ForeignKey('master_setup.Country', null=True, blank=True, on_delete=models.CASCADE, related_name='users')
    state = models.ForeignKey('master_setup.State', null=True, blank=True, on_delete=models.CASCADE, related_name='users')
    address = models.TextField(null=True, blank=True, help_text='Address')    
    hire_date = models.DateField(null=True, blank=True, help_text='Hire date')
    original_hire_date = models.DateField(null=True, blank=True, help_text='Original hire date')
    termination_date = models.DateField(null=True, blank=True, help_text='Termination date')
    def __str__(self):
        return self.username
