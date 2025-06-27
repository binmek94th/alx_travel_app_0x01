import os

import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Listing, Booking, Payment
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


class InitiatePaymentAPIView(APIView):
    def post(self, request):
        chapa_secret_key = os.getenv('CHAPA_SECRET_KEY')
        if not chapa_secret_key:
            return Response({"error": "Chapa secret key not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        booking_reference = request.data.get("booking_reference")
        amount = request.data.get("amount")
        customer_email = request.data.get("email")

        if not booking_reference or not amount or not customer_email:
            return Response({"error": "Missing required payment data."}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            "amount": amount,
            "currency": "ETB",
            "email": customer_email,
            "tx_ref": booking_reference,
            "callback_url": "https://yourdomain.com/api/payments/verify/",
            "return_url": "https://yourdomain.com/payment-success/",
        }

        headers = {
            "Authorization": f"Bearer {chapa_secret_key}",
            "Content-Type": "application/json"
        }

        response = requests.post("https://api.chapa.co/v1/transaction/initialize", json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            payment, created = Payment.objects.get_or_create(
                booking_reference=booking_reference,
                defaults={
                    "amount": amount,
                    "status": "Pending",
                    "transaction_id": data.get("data", {}).get("id")
                }
            )
            return Response({"payment_url": data.get("data", {}).get("checkout_url")})

        return Response({"error": "Failed to initialize payment."}, status=status.HTTP_400_BAD_REQUEST)


class VerifyPaymentAPIView(APIView):
    def get(self, request):
        chapa_secret_key = os.getenv('CHAPA_SECRET_KEY')
        tx_ref = request.query_params.get('tx_ref')
        transaction_id = request.query_params.get('transaction_id')

        if not tx_ref or not transaction_id:
            return Response({"error": "Missing transaction info."}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            "Authorization": f"Bearer {chapa_secret_key}",
        }

        url = f"https://api.chapa.co/v1/transaction/verify/{transaction_id}"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            payment_status = data.get("data", {}).get("status")

            try:
                payment = Payment.objects.get(booking_reference=tx_ref)
                if payment_status == "success":
                    payment.status = "Completed"
                elif payment_status == "failed":
                    payment.status = "Failed"
                payment.save()
            except Payment.DoesNotExist:
                return Response({"error": "Payment record not found."}, status=status.HTTP_404_NOT_FOUND)

            return Response({"status": payment.status})

        return Response({"error": "Failed to verify payment."}, status=status.HTTP_400_BAD_REQUEST)
