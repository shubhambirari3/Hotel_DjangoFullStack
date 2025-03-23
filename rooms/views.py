from django.shortcuts import render, get_object_or_404
from .models import Room, RoomCategory
from feedback.forms import FeedbackForm
from blog.models import Blog

def home(request):
    rooms = Room.objects.all()  # Fetch first 6 rooms
    blogs = Blog.objects.all()  # Fetch first 6 blogs
    context = {
        'rooms': rooms,
        'blogs': blogs,
    }
    return render(request, 'index.html', context)

def room_list(request):
    category_name = request.GET.get('category', 'all').lower()
    categories = RoomCategory.objects.all()
    
    if category_name == 'all':
        rooms = Room.objects.all()
    else:
        rooms = Room.objects.filter(category__name__iexact=category_name)
    
    context = {
        'rooms': rooms,
        'categories': categories,
        'selected_category': category_name,
    }
    return render(request, 'rooms/rooms.html', context)



def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    similar_rooms = Room.objects.exclude(id=room_id)
    feedback_form = FeedbackForm(user=request.user)
    
    context = {
        'room': room,
        'similar_rooms': similar_rooms,
        'feedback_form': feedback_form,
    }
    return render(request, 'rooms/roomdetail.html', context)