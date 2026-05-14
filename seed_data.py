import os
import random
from datetime import timedelta
import django
from django.utils import timezone

# 1. INISIALISASI DJANGO ENVIRONMENT
# GANTI 'myproject.settings' dengan nama folder konfigurasi proyek Anda!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basdut_adventure.settings')
django.setup()

# Import model setelah django.setup() dijalankan
# GANTI 'myapp' dengan nama aplikasi Django Anda!
from django.contrib.auth.hashers import make_password
from ticket_category.models import Event, Organizer, UserAccount, Venue


def run_seed():
    print("Mulai menghapus data lama...")
    # Hapus data lama agar tidak terjadi duplikasi saat skrip dijalankan berkali-kali
    Event.objects.all().delete()
    Organizer.objects.all().delete()
    Venue.objects.all().delete()
    UserAccount.objects.all().delete()
    print("Data lama berhasil dihapus!\n")

    print("1. Membuat User Account...")
    users_data = [
        {"username": "event_manager_1", "password": "supersecretpassword1"},
        {"username": "konser_promotor", "password": "supersecretpassword2"},
    ]
    created_users = []
    for u in users_data:
        # Disarankan menggunakan make_password agar password dienkripsi (hashing)
        user = UserAccount.objects.create(
            username=u["username"], 
            password=make_password(u["password"])
        )
        created_users.append(user)
        print(f"  -> User dibuat: {user.username}")

    print("\n2. Membuat Venue...")
    venues_data = [
        {
            "venue_name": "Stadion Gelora Bung Karno",
            "capacity": 77193,
            "address": "Jl. Pintu Satu Senayan",
            "city": "Jakarta",
        },
        {
            "venue_name": "Jakarta Convention Center",
            "capacity": 5000,
            "address": "Jl. Gatot Subroto",
            "city": "Jakarta",
        },
        {
            "venue_name": "Indonesia Convention Exhibition (ICE)",
            "capacity": 10000,
            "address": "Jl. BSD Grand Boulevard",
            "city": "Tangerang",
        },
    ]
    created_venues = []
    for v in venues_data:
        venue = Venue.objects.create(**v)
        created_venues.append(venue)
        print(f"  -> Venue dibuat: {venue.venue_name}")

    print("\n3. Membuat Organizer...")
    organizers_data = [
        {
            "organizer_name": "Sound Rhythm Production",
            "contact_email": "info@soundrhythm.id",
            "user": created_users[0],  # Relasi ke user 1
        },
        {
            "organizer_name": "Dyandra Promosindo",
            "contact_email": "contact@dyandra.com",
            "user": created_users[1],  # Relasi ke user 2
        },
    ]
    created_organizers = []
    for o in organizers_data:
        organizer = Organizer.objects.create(**o)
        created_organizers.append(organizer)
        print(f"  -> Organizer dibuat: {organizer.organizer_name}")

    print("\n4. Membuat Event...")
    now = timezone.now()
    events_data = [
        {
            "event_title": "Mega Konser Akhir Tahun",
            "event_datetime": now + timedelta(days=30),
            "venue": created_venues[0],  # GBK
            "organizer": created_organizers[0],
        },
        {
            "event_title": "Indonesia Tech Expo 2026",
            "event_datetime": now + timedelta(days=60),
            "venue": created_venues[1],  # JCC
            "organizer": created_organizers[1],
        },
        {
            "event_title": "Pameran Otomotif Internasional",
            "event_datetime": now + timedelta(days=90),
            "venue": created_venues[2],  # ICE BSD
            "organizer": created_organizers[1],
        },
    ]
    for e in events_data:
        event = Event.objects.create(**e)
        print(f"  -> Event dibuat: {event.event_title} di {event.venue.venue_name}")

    print("\n=== Proses Seeding Data Selesai Sukses! ===")


if __name__ == '__main__':
    run_seed()