from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

from .models import Destination, ContactMessage, Inquiry
from .email_service import (
    notify_contact_submitted,
    notify_inquiry_submitted,
    notify_flight_booking,
    notify_newsletter_subscription,
    notify_user_login,
)


def home(request):
    context = {'year': datetime.now().year}
    return render(request, 'home.html', context)


def destinations(request):
    return render(request, 'destinations.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            send_mail(
                f'New contact from {name}',
                f'Email: {email}\n\nMessage:\n{message}',
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_NOTIFICATION_EMAIL],
                fail_silently=True,
            )
            notify_contact_submitted(name, email, message)
            return redirect('contact_success')

    return render(request, 'contact.html')


def contact_success(request):
    return render(request, 'contact_success.html')


def inquiry(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        destination = request.POST.get('destination', '').strip()
        start_date = request.POST.get('start_date', '').strip()
        end_date = request.POST.get('end_date', '').strip()
        message = request.POST.get('message', '').strip()
        dates = f"{start_date} to {end_date}" if start_date and end_date else start_date or end_date or ''

        if name and email:
            try:
                date_obj = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
            except (ValueError, TypeError):
                date_obj = None

            Inquiry.objects.create(
                name=name, email=email,
                date=date_obj or datetime.now().date(),
                message=f"Destination: {destination}\nDates: {dates}\n\n{message}"
            )
            notify_inquiry_submitted(name, email, destination, dates, message)
            return render(request, 'inquiry_success.html', {'name': name})

    destinations_list = [
        'Kerala Backwaters', 'Delhi', 'Agra', 'Jaipur', 'Jaisalmer', 'Jodhpur',
        'Udaipur', 'Varanasi', 'Ladakh', 'Goa', 'Ranthambore', 'Meghalaya',
        'Amritsar', 'Rishikesh', 'Kolkata', 'Darjeeling', 'Mumbai'
    ]
    preselected = request.GET.get('destination', '')
    return render(request, 'inquiry.html', {
        'destinations': destinations_list,
        'preselected_destination': preselected
    })


def about(request):
    return render(request, 'about.html')


def search(request):
    query = request.GET.get('q', '')
    destinations_list = [
        {'name': 'Ladakh', 'description': 'Snowy mountains'},
        {'name': 'Goa', 'description': 'Beaches and nightlife'},
        {'name': 'Kerala', 'description': 'Backwaters'},
    ]
    results = [d for d in destinations_list if query.lower() in d['name'].lower()]
    return render(request, 'search_results.html', {'query': query, 'results': results})


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            send_mail(
                'New Newsletter Subscription',
                f'New subscriber: {email}',
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_NOTIFICATION_EMAIL],
                fail_silently=True,
            )
            notify_newsletter_subscription(email)
            return redirect('subscribe_success')

    return render(request, 'subscribe.html')


def subscribe_success(request):
    return render(request, 'subscribe_success.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            notify_user_login(username)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'login.html')


def flight_booking(request):
    success = None
    if request.method == 'POST':
        from_city = request.POST.get('from', '').strip()
        to_city = request.POST.get('to', '').strip()
        date_val = request.POST.get('date', '').strip()
        passengers = request.POST.get('passengers', '1').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()

        if from_city and to_city and date_val:
            notify_flight_booking(from_city, to_city, date_val, passengers, email, name)
            success = f"Booking request received! We'll confirm your flight from {from_city} to {to_city} for {passengers} passenger(s) on {date_val}."
            if email:
                success += " Check your email for confirmation details."

    return render(request, 'flight_booking.html', {'success': success})


# Destination detail views
def kerala(request): return render(request, 'detail_kerala.html')
def varanasi(request): return render(request, 'detail_varanasi.html')
def ladakh(request): return render(request, 'detail_ladakh.html')
def goa(request): return render(request, 'detail_goa.html')
def ranthambore(request): return render(request, 'detail_ranthambore.html')
def meghalaya(request): return render(request, 'detail_meghalaya.html')
def amritsar(request): return render(request, 'detail_amritsar.html')
def rishikesh(request): return render(request, 'detail_rishikesh.html')
def delhi(request): return render(request, 'detail_delhi.html')
def agra(request): return render(request, 'detail_agra.html')
def jaipur(request): return render(request, 'detail_jaipur.html')
def jaisalmer(request): return render(request, 'detail_jaisalmer.html')
def jodhpur(request): return render(request, 'detail_jodhpur.html')
def udaipur(request): return render(request, 'detail_udaipur.html')
def kolkata(request): return render(request, 'detail_kolkata.html')
def darjeeling(request): return render(request, 'detail_darjeeling.html')
def mumbai(request): return render(request, 'detail_mumbai.html')
