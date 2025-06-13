from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer

class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Listings.
    Provides CRUD operations:
    - list: GET /api/listings/
    - create: POST /api/listings/
    - retrieve: GET /api/listings/{id}/
    - update: PUT /api/listings/{id}/
    - destroy: DELETE /api/listings/{id}/
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Bookings.
    Provides CRUD operations:
    - list: GET /api/bookings/
    - create: POST /api/bookings/
    - retrieve: GET /api/bookings/{id}/
    - update: PUT /api/bookings/{id}/
    - destroy: DELETE /api/bookings/{id}/
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
