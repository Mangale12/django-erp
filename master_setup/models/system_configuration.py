import django.db.models as models


class SystemConfiguration(models.Model):
    parameter_name = models.CharField(max_length=100)
    parameter_value = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.parameter_name

    class Meta:
        db_table = 'system_configuration'