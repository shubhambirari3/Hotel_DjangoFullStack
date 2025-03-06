from django.db import models


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

    def __str__(self):
        return self.name