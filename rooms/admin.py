from django.contrib import admin
from .models import Room, RoomCategory ,RoomImage

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1  # Number of empty image fields to display by default
    fields = ('image',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'capacity', 'size', 'price')
    list_filter = ('category', 'name')

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ('room', 'image')
    list_filter = ('room',  )