from django.shortcuts import render
from .models import Room, RoomCategory

def room_list(request):
    # Get the selected category from the URL query parameter (default to 'all')
    category_name = request.GET.get('category', 'all')
    
    # Filter rooms based on category, or show all if 'all' is selected
    if category_name == 'all':
        rooms = Room.objects.all()
    else:
        rooms = Room.objects.filter(category__name__iexact=category_name)
    
    # Get all categories for the filter buttons
    categories = RoomCategory.objects.all()
    
    # Context to pass to the template
    context = {
        'rooms': rooms,
        'categories': categories,
        'selected_category': category_name,
    }
    return render(request, 'rooms/rooms.html', context)