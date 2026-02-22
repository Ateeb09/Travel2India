from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField()
    price = models.DecimalField(max_digits=8, decimal_places=2) 

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class FlightBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    destination = models.CharField(max_length=100)
    travel_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    """Razorpay payment record."""
    order_id = models.CharField(max_length=100, unique=True)
    amount_paise = models.PositiveIntegerField()
    amount_inr = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='INR')
    description = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default='created')  # created, attempted, captured, failed
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_id} - {self.status}"

