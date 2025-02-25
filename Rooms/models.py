from django.db import models

# Create your models here.
class Room(models.Model):

     # Define choices for room categories
    ECONOMY = 'EC'
    STANDARD = 'ST'
    LUXE = 'LX'
    ALL_ROOMS = 'AL'
    ROOM_CATEGORIES = [
        (ECONOMY, 'Economy'),
        (STANDARD, 'Standard'),
        (LUXE, 'Luxe'),
        (ALL_ROOMS, 'All Rooms'),
    ]

    # Define choices for room types
    SINGLE_BED = 'SB'
    DOUBLE_BED = 'DB'
    ROOM_TYPES = [
        (SINGLE_BED, 'Single bed'),
        (DOUBLE_BED, 'Double Bed'),
    ]

    category = models.CharField(max_length=100, choices=ROOM_CATEGORIES, default=ALL_ROOMS)
    members = models.PositiveIntegerField()
    room_type = models.CharField(max_length=100,  choices=ROOM_TYPES, default=SINGLE_BED)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
       return f"{self.get_category_display()} - {self.get_room_type_display()}"
