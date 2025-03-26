from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, RoomCategory, Reservation
from feedback.forms import FeedbackForm
from blog.models import Blog
from feedback.models import Feedback
from datetime import date, datetime
from django.contrib import messages

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

def home(request):
    rooms = Room.objects.all()
    blogs = Blog.objects.all()
    feedbacks = Feedback.objects.all().order_by('created_at')[:3]
    context = {
        'rooms': rooms,
        'blogs': blogs,
        'feedbacks': feedbacks,
    }
    return render(request, 'index.html', context)

def about_page(request):
    return render(request, 'about.html')

def room_search(request):
    if request.method == 'GET':
        room_id = request.GET.get('room_id')
        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')
        adults = request.GET.get('adults')

        # Validate inputs
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            adults = int(adults)
            if adults <= 0:
                raise ValueError("Number of adults must be positive.")
        except (ValueError, TypeError):
            messages.error(request, 'Invalid date or adults input.')
            return redirect('rooms:room_detail', room_id=room_id)

        today = date.today()
        if check_in_date < today:
            messages.error(request, 'Check-in date cannot be in the past.')
            return redirect('rooms:room_detail', room_id=room_id)
        if check_out_date <= check_in_date:
            messages.error(request, 'Check-out date must be after check-in date.')
            return redirect('rooms:room_detail', room_id=room_id)

        # Get the selected room
        selected_room = get_object_or_404(Room, id=room_id)

        # Check capacity and availability
        if adults > selected_room.capacity:
            is_available = False
            capacity_exceeded = True
        else:
            capacity_exceeded = False
            # Check for overlapping reservations
            overlapping_reservations = Reservation.objects.filter(
                room=selected_room,
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date
            ).exists()
            is_available = not overlapping_reservations

        # Get all available rooms for the date range and adults
        available_rooms = Room.objects.available_rooms(check_in_date, check_out_date, adults)
        other_available_rooms = available_rooms.exclude(id=selected_room.id)

        context = {
            'selected_room': selected_room,
            'is_available': is_available,
            'capacity_exceeded': capacity_exceeded,
            'other_available_rooms': other_available_rooms,
            'check_in': check_in,
            'check_out': check_out,
            'adults': adults,
        }
        return render(request, 'rooms/roomsearch.html', context)
    else:
        return redirect('rooms:room_list')

def room_booking(request):
    return render(request, 'rooms/roombooking.html')