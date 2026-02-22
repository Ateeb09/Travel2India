from django.contrib import admin
from .models import Destination, ContactMessage, Inquiry, Payment

admin.site.register(Destination)
admin.site.register(ContactMessage)
admin.site.register(Inquiry)
admin.site.register(Payment)

