from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, RoomCategory, Reservation , Coupon
from .forms import BookingForm
from feedback.forms import FeedbackForm
from blog.models import Blog
from feedback.models import Feedback
from datetime import date, datetime
from decimal import Decimal
from django.contrib import messages
from django.db import transaction

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

@login_required
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

@login_required
def room_booking(request):
    if request.method == 'POST':
        if 'first_name' in request.POST:
            # Processing the booking confirmation form from roombooking.html
            form = BookingForm(request.POST)
            room_id = request.POST.get('room_id')
            check_in = request.POST.get('check_in')
            check_out = request.POST.get('check_out')
            adults = request.POST.get('adults')
            coupon_code = request.POST.get('coupon_code', '')
            payment_method = request.POST.get('mphb_gateway_id')
            try:
                room = Room.objects.get(id=room_id)
                check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
                adults = int(adults)
            except (ValueError, Room.DoesNotExist):
                messages.error(request, 'Invalid booking data.')
                return redirect('rooms:room_list')

            num_nights = (check_out_date - check_in_date).days
            if num_nights <= 0:
                messages.error(request, 'Check-out date must be after check-in date.')
                return redirect('rooms:room_list')

            subtotal = room.price * num_nights
            gst = subtotal * Decimal('0.18')
            total = subtotal + gst
            discount = Decimal('0.00')

            # Handle coupon code
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(
                        code=coupon_code,
                        active=True,
                        valid_from__lte=check_in_date,
                        valid_to__gte=check_out_date
                    )
                    discount = (subtotal * coupon.discount_percentage) / Decimal('100')
                    total -= discount
                    messages.success(request, 'Awesome! You just scored a deal with your coupon!')
                except Coupon.DoesNotExist:
                    messages.error(request, 'Invalid or expired coupon code.')

            if form.is_valid():
                with transaction.atomic():
                    if not room.is_available(check_in_date, check_out_date):
                        messages.error(request, 'The room is no longer available.')
                        return redirect('rooms:room_list')

                    reservation = form.save(commit=False)
                    reservation.room = room
                    reservation.check_in_date = check_in_date
                    reservation.check_out_date = check_out_date
                    reservation.adults = adults
                    reservation.subtotal = subtotal
                    reservation.gst = gst
                    reservation.total = total
                    reservation.discount_applied = discount
                    reservation.payment_method = payment_method
                    if coupon_code and discount > 0:
                        reservation.coupon = coupon
                    if request.user.is_authenticated:
                        reservation.user = request.user
                    reservation.save()

                messages.success(request, 'Booking successful! Welcome! Thank you for choosing our hotel. We hope your stay is comfortable and enjoyable.')
                return redirect('rooms:booking_confirmation', reservation_id=reservation.id)
            else:
                context = {
                    'form': form,
                    'room': room,
                    'check_in': check_in,
                    'check_out': check_out,
                    'adults': adults,
                    'num_nights': num_nights,
                    'subtotal': subtotal,
                    'gst': gst,
                    'total': total,
                    'coupon_code': coupon_code,
                }
                return render(request, 'rooms/roombooking.html', context)
        else:
            # Initiating booking from roomsearch.html
            room_id = request.POST.get('room_id')
            check_in = request.POST.get('check_in')
            check_out = request.POST.get('check_out')
            adults = request.POST.get('adults')

            try:
                room = Room.objects.get(id=room_id)
                check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
                adults = int(adults)
            except (ValueError, Room.DoesNotExist):
                messages.error(request, 'Invalid booking data.')
                return redirect('rooms:room_list')

            num_nights = (check_out_date - check_in_date).days
            if num_nights <= 0:
                messages.error(request, 'Check-out date must be after check-in date.')
                return redirect('rooms:room_list')

            subtotal = room.price * num_nights
            gst = subtotal * Decimal('0.18')
            total = subtotal + gst

            form = BookingForm()
            context = {
                'form': form,
                'room': room,
                'check_in': check_in,
                'check_out': check_out,
                'adults': adults,
                'num_nights': num_nights,
                'subtotal': subtotal,
                'gst': gst,
                'total': total,
            }
            return render(request, 'rooms/roombooking.html', context)
    return redirect('rooms:room_list')

def booking_confirmation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    context = {'reservation': reservation}
    return render(request, 'rooms/bookingconfirmation.html', context)