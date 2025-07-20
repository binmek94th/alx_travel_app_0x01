from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ListingViewSet, BookingViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)
router.register('payments', PaymentViewSet)

urlpatterns = [
    # path('payment/', InitiatePaymentAPIView.as_view(), name='initiate-payment'),
] + router.urls
