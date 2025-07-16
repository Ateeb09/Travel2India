"""
URL configuration for travel2india project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # ✅ this includes all the routes from your app
]


# from django.contrib import admin
# from django.urls import path
# from core import views  # assuming your app is named 'core'

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.home, name='home'),
#     path('destinations/', views.destinations, name='destinations'),
#     path('contact/', views.contact, name='contact'),
# ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('kerala/', views.kerala, name='kerala'),
#     path('varanasi/', views.varanasi, name='varanasi'),
#     path('ladakh/', views.ladakh, name='ladakh'),
#     path('goa/', views.goa, name='goa'),
#     path('ranthambore/', views.ranthambore, name='ranthambore'),
#     path('meghalaya/', views.meghalaya, name='meghalaya'),
#     path('amritsar/', views.amritsar, name='amritsar'),
#     path('rishikesh/', views.rishikesh, name='rishikesh'),
#     path('contact/', views.contact, name='contact'),
# ]

# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('core.urls')),  # ← This line is crucial
# ]




