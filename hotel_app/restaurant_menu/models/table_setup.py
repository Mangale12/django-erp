import django.db.models as models

class TableSetup(models.Model):
    name = models.CharField(max_length=256, unique=True, null=True, blank=True, help_text='Name of the table (max 256 characters)')
    seating_capacity = models.IntegerField(blank=True, help_text='Seating capacity of the table')
    location_area = models.CharField(max_length=250, unique=True, null=True, blank=True, help_text='Location area of the table')
    zone = models.ForeignKey('Zone', on_delete=models.CASCADE, null=True, blank=True, help_text='Zone of the table')
    is_active = models.BooleanField(default=True, help_text='Is the table active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the table was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the table was last updated')

    def __str__(self):
        return self.name
