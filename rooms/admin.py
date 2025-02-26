from django.contrib import admin
from .models import RoomCategory, Room

# Register RoomCategory model
@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Columns shown in the list view
    search_fields = ('name',)  # Enable search by category name

# Register Room model
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'capacity', 'size')  # Columns shown
    list_filter = ('category',)  # Filter by category
    search_fields = ('name', 'description')  # Search by name or description
    list_editable = ('price',)  # Edit price directly in the list view