"""
Email notification service for Travel2India.
Sends admin notifications for all user actions on the website.
"""
from django.core.mail import send_mail
from django.conf import settings

# Admin email to receive all notifications
ADMIN_EMAIL = getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', settings.EMAIL_HOST_USER)


def send_admin_notification(subject, message, fail_silently=True):
    """Send notification email to admin for any website action."""
    try:
        send_mail(
            subject=f'[Travel2India] {subject}',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[ADMIN_EMAIL],
            fail_silently=fail_silently,
        )
    except Exception as e:
        if not fail_silently:
            raise e


def notify_contact_submitted(name, email, message):
    """Notify when contact form is submitted."""
    body = f"""New Contact Form Submission
━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {name}
Email: {email}

Message:
{message}
"""
    send_admin_notification('New Contact Message', body)


def notify_inquiry_submitted(name, email, destination, dates, message):
    """Notify when booking inquiry is submitted."""
    body = f"""New Booking Inquiry
━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {name}
Email: {email}
Destination: {destination}
Dates: {dates}

Message:
{message}
"""
    send_admin_notification('New Booking Inquiry', body)


def notify_flight_booking(from_city, to_city, date, passengers, email=None, name=None):
    """Notify when flight booking is submitted."""
    extra = ''
    if name or email:
        extra = f"\nName: {name or 'N/A'}\nEmail: {email or 'N/A'}\n"
    body = f"""New Flight Booking Request
━━━━━━━━━━━━━━━━━━━━━━━━━
From: {from_city}
To: {to_city}
Date: {date}
Passengers: {passengers}
{extra}
"""
    send_admin_notification('New Flight Booking', body)


def notify_newsletter_subscription(email):
    """Notify when someone subscribes to newsletter."""
    body = f"""New Newsletter Subscription
━━━━━━━━━━━━━━━━━━━━━━━━━
Email: {email}
"""
    send_admin_notification('New Newsletter Subscriber', body)


def notify_user_login(username):
    """Notify when a user logs in (optional - can be noisy)."""
    body = f"""User Login
━━━━━━━━━━━━━━━━━━━━━━━━━
Username: {username}
"""
    send_admin_notification('User Logged In', body)


def notify_payment_captured(order_id, amount_inr, email=''):
    """Notify when a payment is successfully captured."""
    body = f"""Payment Received
━━━━━━━━━━━━━━━━━━━━━━━━━
Order ID: {order_id}
Amount: ₹{amount_inr}
Email: {email or 'N/A'}
"""
    send_admin_notification('Payment Received', body)
