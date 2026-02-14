from django.db import models
from hotel_app.rooms.models import Room
class RoomRate(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name', help_text='Enter Name', blank=True, null=True)
    code = models.CharField(max_length=255, verbose_name='Code', help_text='Enter Code', blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Rate', help_text='Enter Rate')
    capacity = models.IntegerField(verbose_name='Capacity', help_text='Enter Capacity')
    extra_bed_charge = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Extra Bed Charge', help_text='Enter Extra Bed Charge')
    tax_type = models.ForeignKey('master_setup.TaxType', on_delete=models.CASCADE, verbose_name='Tax Type', help_text='Select Tax Type')
    is_active = models.BooleanField(default=True, verbose_name='Is Active', help_text='Is Active')    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Room Rate'
        verbose_name_plural = 'Room Rates'
        ordering = ['name']