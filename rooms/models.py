from django.db import models


class RoomCategory(models.Model):
    name = models.CharField(max_length=50, unique=True) # e.g., "Economy", "Luxe", "Standard"
    description = models.TextField(blank=True)           

    def __str__(self):
        return self.name

# Model for individual rooms
class Room(models.Model):
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)              # e.g., "Deluxe Room", "Standard Room"
    # Fixed choices for size
    SIZE_CHOICES = [
        ('single', 'Single Bedroom'),
        ('double', 'Double Bedroom'),
        ('triple', 'Triple Bedroom'),
    ]
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)  # e.g., "Single Bed"
    capacity = models.IntegerField()                     # e.g., 2 (adults)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., 49.00
    description = models.TextField()                     # Room description
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)  # Room image

    def __str__(self):
        return f"{self.name} ({self.category.name})"