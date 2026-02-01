import django.db.models as models

class SalaryStructure(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the salary structure (max 256 characters)')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Basic salary')
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='HRA')
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Special allowance')
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Medical allowance')
    conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Conveyance allowance')
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Tax')
    pf = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='PF')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the salary structure was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the salary structure was last updated')
    
    def __str__(self):
        return self.name
