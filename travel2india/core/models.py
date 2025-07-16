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

