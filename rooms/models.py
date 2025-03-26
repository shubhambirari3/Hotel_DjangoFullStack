from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class RoomManager(models.Manager):
    def available_rooms(self, check_in, check_out, adults):
        # Get IDs of rooms with overlapping reservations
        reserved_rooms = Reservation.objects.filter(
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        ).values_list('room_id', flat=True)
        
        # Return rooms with sufficient capacity and no overlapping reservations
        return self.filter(
            capacity__gte=adults
        ).exclude(
            id__in=reserved_rooms
        )
    
class RoomCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    SIZE_CHOICES = (
        ('S', 'Single Bedroom'),
        ('D', 'Double Bedroom'),
        ('T', 'Triple Bedroom'),
    )
    
    name = models.CharField(max_length=100)
    category = models.ForeignKey(RoomCategory, on_delete=models.SET_NULL, null=True)
    capacity = models.PositiveIntegerField()  # Number of adults
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)  # Saves to media/rooms/
    objects = RoomManager()  # Assign the custom manager to objects

    def __str__(self):
        return self.name
    

class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images/')

    def __str__(self):
        return f"Image for {self.room.name}"
    


    

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    adults = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Reservation for {self.room.name} from {self.check_in_date} to {self.check_out_date}"