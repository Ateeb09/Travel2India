from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_http_methods
from datetime import datetime
from decimal import Decimal

from .models import Destination, ContactMessage, Inquiry, Payment
from .email_service import (
    notify_contact_submitted,
    notify_inquiry_submitted,
    notify_flight_booking,
    notify_newsletter_subscription,
    notify_user_login,
    notify_payment_captured,
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


# All 17 destinations: name, URL name, image, and search keywords
SEARCH_DESTINATIONS = [
    {'name': 'Kerala Backwaters', 'url_name': 'kerala', 'image': 'kerala.jpg', 'keywords': 'kerala backwaters alleppey houseboat'},
    {'name': 'Delhi', 'url_name': 'delhi', 'image': 'delhi.jpg', 'keywords': 'delhi capital red fort'},
    {'name': 'Agra', 'url_name': 'agra', 'image': 'agra.jpg', 'keywords': 'agra taj mahal'},
    {'name': 'Jaipur', 'url_name': 'jaipur', 'image': 'jaipur.jpg', 'keywords': 'jaipur pink city rajasthan'},
    {'name': 'Jaisalmer', 'url_name': 'jaisalmer', 'image': 'jaisalmer.jpg', 'keywords': 'jaisalmer golden city desert'},
    {'name': 'Jodhpur', 'url_name': 'jodhpur', 'image': 'jodhpur.jpg', 'keywords': 'jodhpur blue city'},
    {'name': 'Udaipur', 'url_name': 'udaipur', 'image': 'udaipur.jpg', 'keywords': 'udaipur city of lakes'},
    {'name': 'Varanasi', 'url_name': 'varanasi', 'image': 'varanasi.jpg', 'keywords': 'varanasi banaras ganges'},
    {'name': 'Ladakh', 'url_name': 'ladakh', 'image': 'ladakh.jpg', 'keywords': 'ladakh leh pangong'},
    {'name': 'Goa', 'url_name': 'goa', 'image': 'goa.jpg', 'keywords': 'goa beaches'},
    {'name': 'Ranthambore', 'url_name': 'ranthambore', 'image': 'ranthambore.jpg', 'keywords': 'ranthambore tiger safari'},
    {'name': 'Meghalaya', 'url_name': 'meghalaya', 'image': 'meghalaya.jpg', 'keywords': 'meghalaya cherrapunji shillong'},
    {'name': 'Amritsar', 'url_name': 'amritsar', 'image': 'amritsar.jpg', 'keywords': 'amritsar golden temple'},
    {'name': 'Rishikesh', 'url_name': 'rishikesh', 'image': 'rishikesh.jpg', 'keywords': 'rishikesh yoga rafting'},
    {'name': 'Kolkata', 'url_name': 'kolkata', 'image': 'kolkata.jpg', 'keywords': 'kolkata calcutta'},
    {'name': 'Darjeeling', 'url_name': 'darjeeling', 'image': 'darjeeling.jpg', 'keywords': 'darjeeling tea hills'},
    {'name': 'Mumbai', 'url_name': 'mumbai', 'image': 'mumbai.jpg', 'keywords': 'mumbai bombay'},
]


def search(request):
    query = (request.GET.get('q', '') or '').strip().lower()
    if not query:
        return render(request, 'search_results.html', {'query': '', 'results': [], 'all_destinations': SEARCH_DESTINATIONS})

    def matches(d):
        if query in d['name'].lower():
            return True
        return any(query in k for k in d['keywords'].lower().split())

    results = [d for d in SEARCH_DESTINATIONS if matches(d)]

    # Single match → redirect to that destination's beautiful detail page
    if len(results) == 1:
        dest = results[0]
        return redirect(reverse(dest['url_name']))

    return render(request, 'search_results.html', {
        'query': request.GET.get('q', '').strip(),
        'results': results,
        'all_destinations': SEARCH_DESTINATIONS,
    })


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


# ---------- Payment (Razorpay) ----------
def payment_page(request):
    """Show payment page with amount and description."""
    razorpay_key = getattr(settings, 'RAZORPAY_KEY_ID', '') or ''
    return render(request, 'payment.html', {
        'razorpay_key': razorpay_key,
        'payment_enabled': bool(razorpay_key),
    })


@require_http_methods(['POST'])
def create_order(request):
    """Create Razorpay order and return order_id, amount, key for checkout."""
    if not getattr(settings, 'RAZORPAY_KEY_ID', None) or not getattr(settings, 'RAZORPAY_KEY_SECRET', None):
        return JsonResponse({'error': 'Payment not configured'}, status=503)
    try:
        amount_inr = Decimal(request.POST.get('amount', 0))
        if amount_inr < 1:
            return JsonResponse({'error': 'Amount must be at least ₹1'}, status=400)
        description = (request.POST.get('description', '') or 'Travel2India - Trip/Package payment')[:255]
        email = (request.POST.get('email', '') or '').strip()
    except Exception:
        return JsonResponse({'error': 'Invalid amount'}, status=400)
    amount_paise = int(amount_inr * 100)
    try:
        import razorpay
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        data = {
            'amount': amount_paise,
            'currency': 'INR',
            'receipt': f't2i_{datetime.now().strftime("%Y%m%d%H%M%S")}',
        }
        order = client.order.create(data=data)
        order_id = order['id']
        Payment.objects.create(
            order_id=order_id,
            amount_paise=amount_paise,
            amount_inr=amount_inr,
            description=description,
            status='created',
            email=email,
        )
        return JsonResponse({
            'order_id': order_id,
            'amount': amount_paise,
            'currency': 'INR',
            'key_id': settings.RAZORPAY_KEY_ID,
            'description': description,
        })
    except Exception as e:
        return JsonResponse({'error': str(e) or 'Failed to create order'}, status=500)


@require_http_methods(['POST'])
def verify_payment(request):
    """Verify Razorpay signature and mark payment as captured."""
    if not getattr(settings, 'RAZORPAY_KEY_SECRET', None):
        return JsonResponse({'success': False, 'error': 'Payment not configured'}, status=503)
    razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_order_id = request.POST.get('razorpay_order_id', '')
    razorpay_signature = request.POST.get('razorpay_signature', '')
    if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
        return JsonResponse({'success': False, 'error': 'Missing payment data'}, status=400)
    try:
        import razorpay
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        client.utility.verify_payment_signature({
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_signature': razorpay_signature,
        })
        pay = Payment.objects.get(order_id=razorpay_order_id)
        pay.razorpay_payment_id = razorpay_payment_id
        pay.razorpay_signature = razorpay_signature
        pay.status = 'captured'
        pay.save()
        notify_payment_captured(razorpay_order_id, str(pay.amount_inr), pay.email)
        return JsonResponse({'success': True, 'order_id': razorpay_order_id})
    except Payment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found'}, status=400)
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({'success': False, 'error': 'Invalid signature'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
