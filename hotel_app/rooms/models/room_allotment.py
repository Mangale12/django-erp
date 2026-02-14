from django.db import models

class RoomAllotment(models.Model):
    booking = models.ForeignKey("reception.booking", on_delete=models.CASCADE, related_name="room_allotments", null=True, blank=True)
    room = models.ForeignKey("rooms.room", on_delete=models.CASCADE, related_name="room_allotments")
    alloted_by = models.ForeignKey("auth.user", on_delete=models.CASCADE, related_name="room_allotments")
    alloted_at = models.DateTimeField(auto_now_add=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
