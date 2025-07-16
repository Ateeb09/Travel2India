from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # For now, we just print it — later we’ll save or send email
        print(f"New message from {name} ({email}): {message}")
        return HttpResponseRedirect(reverse('contact_success'))

    return render(request, 'contact.html')

def contact_success(request):
    return render(request, 'contact_success.html')


   

def home(request):
    return render(request, 'home.html')

def kerala(request):
    return render(request, 'detail_kerala.html')

def varanasi(request):
    return render(request, 'detail_varanasi.html')

def ladakh(request):
    return render(request, 'detail_ladakh.html')

def goa(request):
    return render(request, 'detail_goa.html')

def ranthambore(request):
    return render(request, 'detail_ranthambore.html')

def meghalaya(request):
    return render(request, 'detail_meghalaya.html')

def amritsar(request):
    return render(request, 'detail_amritsar.html')

def rishikesh(request):
    return render(request, 'detail_rishikesh.html')

def delhi(request):
    return render(request, 'detail_delhi.html')

def agra(request):
    return render(request, 'detail_agra.html')

def jaipur(request):
    return render(request, 'detail_jaipur.html')

def jaisalmer(request):
    return render(request, 'detail_jaisalmer.html')

def jodhpur(request):
    return render(request, 'detail_jodhpur.html')

def udaipur(request):
    return render(request, 'detail_udaipur.html')

def kolkata(request):
    return render(request, 'detail_kolkata.html')

def darjeeling(request):
    return render(request, 'detail_darjeeling.html')

def mumbai(request):
    return render(request, 'detail_mumbai.html')





def home(request):
    return render(request, 'home.html')

def destinations(request):
    return render(request, 'destinations.html')

def contact(request):
    return render(request, 'contact.html')



def inquiry(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        destination = request.POST.get('destination')
        dates = request.POST.get('dates')
        message = request.POST.get('message')
        
        # For now, just print it in console (later we can save to DB or send email)
        print("Booking Inquiry Received:")
        print("Name:", name)
        print("Email:", email)
        print("Destination:", destination)
        print("Dates:", dates)
        print("Message:", message)

      
        return render(request, 'inquiry_success.html', {'name': name})
    
    return render(request, 'inquiry.html')


def about(request):
    return render(request, 'about.html')



# def search(request):
#     query = request.GET.get('q', '')  # getting search query from GET request
#     return render(request, 'search_results.html', {'query': query})



from django.shortcuts import render
from .models import Destination  # if you have a model, else we can use hardcoded data

def search(request):
    query = request.GET.get('q', '')
    destinations = [
        {'name': 'Ladakh', 'description': 'Snowy mountains'},
        {'name': 'Goa', 'description': 'Beaches and nightlife'},
        {'name': 'Kerala', 'description': 'Backwaters'},
    ]
    results = []
    for destination in destinations:
        if query.lower() in destination['name'].lower():
            results.append(destination)
    
    return render(request, 'search_results.html', {'query': query, 'results': results})


from django.shortcuts import render, redirect
from django.contrib import messages

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Here, you could save the email to the database or send it to your email
        print("New subscriber:", email)
        messages.success(request, "Thank you for subscribing!")
        return redirect('home')


from datetime import datetime

def home(request):
    context = {
        'year': datetime.now().year,
        # your other context here
    }
    return render(request, 'home.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials, try again!')
    return render(request, 'login.html')



def flight_booking(request):
    if request.method == "POST":
        # You can handle booking logic here
        from_city = request.POST['from']
        to_city = request.POST['to']
        date = request.POST['date']
        passengers = request.POST['passengers']
        # For now, just display a success message (no database)
        success = f"Flight booked from {from_city} to {to_city} for {passengers} passenger(s) on {date}."
        return render(request, 'flight_booking.html', {'success': success})
    return render(request, 'flight_booking.html')



# from django.shortcuts import render, redirect
# from django.core.mail import send_mail
from .forms import ContactForm, InquiryForm, FlightBookingForm
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                'New Contact Form Submission',
                'Contact Message Details Here...',
                settings.EMAIL_HOST_USER,
                ['ateebahmad009@gmail.com'],
                fail_silently=False,
            )
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def inquiry_view(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            send_mail(
                'New Inquiry Form Submission',
                'Inquiry Message Details Here...',
                settings.EMAIL_HOST_USER,
                ['ateebahmad009@gmail.com'],
                fail_silently=False,
            )
    else:
        form = InquiryForm()
    return render(request, 'inquiry.html', {'form': form})

def flight_booking_view(request):
    if request.method == 'POST':
        form = FlightBookingForm(request.POST)
        if form.is_valid():
            # Process the form data here (save or send email)
            send_mail(
                'New Flight Booking Request',
                'Message Details Here...',
                settings.EMAIL_HOST_USER,  # ✅ Correct usage here
                ['ateebahmad009@gmail.com'],  # Your recipient email
                fail_silently=False,
            )
            # Optionally redirect or show success message
    else:
        form = FlightBookingForm()
    return render(request, 'flight_booking.html', {'form': form})







