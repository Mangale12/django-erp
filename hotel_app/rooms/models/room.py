import django.db.models as models


class Room(models.Model):
    room_number = models.CharField(max_length=256, unique=False, null=True, blank=True, help_text='Room number (max 256 characters)')
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE, related_name='rooms')
    room_category = models.ForeignKey('RoomCategory', on_delete=models.CASCADE, related_name='rooms')
    floor = models.ForeignKey('Floor', on_delete=models.CASCADE, related_name='rooms')
    view_type = models.ForeignKey('RoomViewType', on_delete=models.CASCADE, related_name='rooms')
    amenities = models.ManyToManyField('RoomAmnity', related_name='rooms')
    current_status = models.CharField(max_length=256, unique=False, null=True, blank=True, help_text='Current status of the room (max 256 characters)')
    remarks = models.TextField(unique=False, null=True, blank=True, help_text='Remarks of the room (max 256 characters)')
    is_active = models.BooleanField(default=True, help_text='Is the room active?')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the room was created')
    updated_at = models.DateTimeField(auto_now=True, help_text='Date and time when the room was last updated')
    
    
    def __str__(self):
        return self.room_number