from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import Contact

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, user=request.user)
        if form.is_valid():
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                # For authenticated users, link to user and use profile data
                contact.user = request.user
                contact.name = request.user.get_full_name()
                contact.email = request.user.email
            else:
                # For non-authenticated users, use form data
                contact.name = form.cleaned_data['name']
                contact.email = form.cleaned_data['email']
            contact.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact:contact_us')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm(user=request.user)

    return render(request, 'contact/contact.html', {'form': form})


