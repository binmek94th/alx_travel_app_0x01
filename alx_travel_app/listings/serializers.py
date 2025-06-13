from rest_framework import serializers

from listings.models import Listing, Review, Booking


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['total_price', 'status', 'created_at', 'updated_at']

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("Start date must be before end date.")
        return data

    def create(self, validated_data):
        listing = validated_data['listing']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']

        total_days = (end_date - start_date).days
        total_price = listing.price_per_night * total_days

        validated_data['total_price'] = total_price

        return super().create(validated_data)