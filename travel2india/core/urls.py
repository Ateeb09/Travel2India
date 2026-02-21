from django.urls import path
from . import views

   

urlpatterns = [
    path('', views.home, name='home'),
    path('inquiry/', views.inquiry, name='inquiry'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('search/', views.search, name='search'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('destinations/', views.destinations, name='destinations'), 
    path('login/', views.user_login, name='login'),
    path('about/', views.about, name='about'),
    path('flight-booking/', views.flight_booking, name='flight_booking'),


    # Destination Detail Pages
    path('kerala/', views.kerala, name='kerala'),
    path('varanasi/', views.varanasi, name='varanasi'),
    path('ladakh/', views.ladakh, name='ladakh'),
    path('goa/', views.goa, name='goa'),
    path('ranthambore/', views.ranthambore, name='ranthambore'),
    path('meghalaya/', views.meghalaya, name='meghalaya'),
    path('amritsar/', views.amritsar, name='amritsar'),
    path('rishikesh/', views.rishikesh, name='rishikesh'),
    path('delhi/', views.delhi, name='delhi'),
    path('agra/', views.agra, name='agra'),
    path('jaipur/', views.jaipur, name='jaipur'),
    path('jaisalmer/', views.jaisalmer, name='jaisalmer'),
    path('jodhpur/', views.jodhpur, name='jodhpur'),
    path('udaipur/', views.udaipur, name='udaipur'),
    path('kolkata/', views.kolkata, name='kolkata'),
    path('darjeeling/', views.darjeeling, name='darjeeling'),
    path('mumbai/', views.mumbai, name='mumbai'),
    path('subscribe/success/', views.subscribe_success, name='subscribe_success'),
]
