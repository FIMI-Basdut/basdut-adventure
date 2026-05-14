import os
from datetime import timedelta
import django
from django.utils import timezone


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basdut_adventure.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from dashboard.models import (
    AccountRole, Artist, Customer, Event, EventArtist, OrderPromotion,
    Organizer, Promotion, Role, Seat, Ticket, TicketCategory, TicketOrder,
    UserAccount, Venue
)


def run_seed():
    print("Membersihkan database...")

    Role.objects.all().delete()
    UserAccount.objects.all().delete()
    Venue.objects.all().delete()
    Artist.objects.all().delete()
    Promotion.objects.all().delete()
    print("Database berhasil dibersihkan!\n")

    print("1. Seeding Master Data (Role, Artist, Promo, Venue)...")
    role_admin = Role.objects.create(role_name="Admin")
    role_org = Role.objects.create(role_name="Organizer")
    role_cust = Role.objects.create(role_name="Customer")

    artist1 = Artist.objects.create(artist_name="Tulus", genre="Pop")
    artist2 = Artist.objects.create(artist_name="Dewa 19", genre="Rock")

    now = timezone.now()
    today = now.date()
    
    promo_pct = Promotion.objects.create(
        promo_code="DISCOUNT20", discount_type="PERCENTAGE", discount_value=20.00,
        start_date=today, end_date=today + timedelta(days=30), usage_limit=100
    )
    promo_nom = Promotion.objects.create(
        promo_code="HEMAT50K", discount_type="NOMINAL", discount_value=50000.00,
        start_date=today, end_date=today + timedelta(days=30), usage_limit=50
    )

    venue_gbk = Venue.objects.create(
        venue_name="Stadion Utama GBK", capacity=77000, address="Senayan", city="Jakarta"
    )
    venue_jcc = Venue.objects.create(
        venue_name="JCC Plenary Hall", capacity=5000, address="Senayan", city="Jakarta"
    )
    venue_ice = Venue.objects.create(
        venue_name="ICE BSD Hall 5-6", capacity=10000, address="BSD City", city="Tangerang"
    )

    print("2. Seeding Seats...")
    seat1 = Seat.objects.create(section="VIP A", row_number="A", seat_number="1", venue=venue_gbk)
    seat2 = Seat.objects.create(section="VIP A", row_number="A", seat_number="2", venue=venue_gbk)
    seat3 = Seat.objects.create(section="FESTIVAL", row_number="0", seat_number="0", venue=venue_jcc)

    print("3. Seeding Users, Customers & Organizers...")
    u_org = UserAccount.objects.create(username="promotor_hits", password=make_password("pass123"))
    AccountRole.objects.create(user=u_org, role=role_org)
    organizer = Organizer.objects.create(organizer_name="Dyandra Promosindo", contact_email="info@dyandra.com", user=u_org)

    u_cust1 = UserAccount.objects.create(username="budi_p", password=make_password("pass123"))
    AccountRole.objects.create(user=u_cust1, role=role_cust)
    customer1 = Customer.objects.create(full_name="Budi Perkasa", phone_number="0812345678", user=u_cust1)

    print("4. Seeding Events & Artists Relations...")
    event1 = Event.objects.create(
        event_title="Konser Monokrom Tulus", event_datetime=now + timedelta(days=15),
        venue=venue_gbk, organizer=organizer
    )
    EventArtist.objects.create(event=event1, artist=artist1, role="Main Performer")

    event2 = Event.objects.create(
        event_title="Pesta Rakyat Dewa 19", event_datetime=now + timedelta(days=20),
        venue=venue_jcc, organizer=organizer
    )
    EventArtist.objects.create(event=event2, artist=artist2, role="Band Utama")

    print("5. Seeding Ticket Categories...")
    cat_vip = TicketCategory.objects.create(category_name="VIP", quota=100, price=1500000.00, tevent=event1)
    cat_fest = TicketCategory.objects.create(category_name="Festival", quota=1000, price=500000.00, tevent=event1)
    cat_dewa = TicketCategory.objects.create(category_name="Presale 1", quota=500, price=750000.00, tevent=event2)

    print("6. Seeding Transaksi (Orders, Tiket, Relasi Kursi & Promo)...")

    order1 = TicketOrder.objects.create(
        order_date=now, payment_status="PAID", total_amount=5, customer=customer1 
    )
    OrderPromotion.objects.create(order=order1, promotion=promo_pct)

    t1 = Ticket.objects.create(ticket_code="TULUS-VIP-001", tcategory=cat_vip, torder=order1)
    t1.seats.add(seat1) # Menyuntikkan relasi ke tabel HAS_RELATIONSHIP

    t2 = Ticket.objects.create(ticket_code="TULUS-VIP-002", tcategory=cat_vip, torder=order1)
    t2.seats.add(seat2)

    order2 = TicketOrder.objects.create(
        order_date=now, payment_status="PAID", total_amount=4, customer=customer1 
    )
    OrderPromotion.objects.create(order=order2, promotion=promo_nom)
    t3 = Ticket.objects.create(ticket_code="TULUS-FEST-001", tcategory=cat_fest, torder=order2)

    print("\n=== Proses Seeding Data Lengkap Selesai Sukses! ===")


if __name__ == '__main__':
    run_seed()