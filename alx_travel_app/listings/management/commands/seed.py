import random
from datetime import timedelta, date

from django.core.management.base import BaseCommand
from faker import Faker

from listings.models import Listing, Booking, Review

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with sample listings, bookings, and reviews."

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing old data...")
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()

        self.stdout.write("Seeding database...")

        listings = []
        for _ in range(10):
            listing = Listing.objects.create(
                name=fake.company(),
                description=fake.text(),
                location=fake.city(),
                price_per_night=round(random.uniform(50, 300), 2)
            )
            listings.append(listing)

            for _ in range(random.randint(1, 3)):
                start_date = fake.date_between(start_date='-2y', end_date='today')
                end_date = start_date + timedelta(days=random.randint(2, 14))
                Booking.objects.create(
                    listing=listing,
                    total_price=round((listing.price_per_night * (end_date - start_date).days), 2),
                    status=random.choice(['pending', 'confirmed', 'cancelled']),
                    start_date=start_date,
                    end_date=end_date,
                )

            for _ in range(random.randint(1, 5)):
                Review.objects.create(
                    listing=listing,
                    rating=random.randint(1, 5),
                    comment=fake.paragraph()
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(listings)} listings.'))
