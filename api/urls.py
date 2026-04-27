from django.urls import path
from . import views

urlpatterns = [
    path('photographers/', views.handle_photographers),
    path('photographers/<str:pk>/', views.handle_photographer_detail),
    path('bookings/', views.handle_bookings),
    path('bookings/<str:pk>/', views.handle_booking_detail),
]
