from django.db import models 

class KitchenType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = "mst_kitchen_types"
        verbose_name = "Kitchen Type"
        verbose_name_plural = "Kitchen Types"
        
    def __str__(self):
        return self.name