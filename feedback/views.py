from django.shortcuts import render, redirect
from .forms import FeedbackForm
from django.urls import reverse
from django.contrib import messages
from .models import Feedback

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)

            # Assign user only if authenticated
            if request.user.is_authenticated:
                feedback.user = request.user

            feedback.save()
            messages.success(request, 'Feedback submitted successfully.')
            return redirect(reverse('feedback:feedback_list'))  
        else:
            messages.error(request, 'Invalid form submission. Please try again.')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback.html', {'form': form})

# ✅ Add this view to display all feedback
def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks})
