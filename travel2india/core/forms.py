from django import forms
from .models import ContactMessage, Inquiry, FlightBooking

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = '__all__'  # This means include all fields from the model

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = '__all__'

class FlightBookingForm(forms.ModelForm):
    class Meta:
        model = FlightBooking
        fields = '__all__'
