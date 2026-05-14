from datetime import date
from django.db.models import Count, Max, Sum
from django.shortcuts import render
from django.utils import timezone

# Sesuaikan import model dengan struktur folder app Anda
from .models import (
    Event,
    OrderPromotion,
    Promotion,
    Seat,
    Ticket,
    UserAccount,
    Venue
)




# Create your views here.

def show_dashboard_customer(request):
    return render(request, 'dashboard_customer.html')
def show_dashboard_organizer(request):
    return render(request, 'dashboard_organizer.html')
def show_dashboard_admin(request):

    total_users = UserAccount.objects.count()


    total_events = Event.objects.count()


    omzet_data = Ticket.objects.aggregate(total_omzet=Sum("tcategory__price"))
    total_omzet = omzet_data["total_omzet"] or 0


    def format_omzet(amount):
        if amount >= 1_000_000_000:
            return f"Rp {amount / 1_000_000_000:.1f}M"
        elif amount >= 1_000_000:
            return f"Rp {amount / 1_000_000:.1f}Jt"
        elif amount > 0:
            return f"Rp {amount:,.0f}".replace(",", ".")
        return "Rp 0"

    formatted_omzet = format_omzet(total_omzet)


    today = timezone.now().date()
    active_promos = Promotion.objects.filter(
        end_date__gt=today, usage_limit__gt=0
    ).count()


    total_venues = Venue.objects.count()


    reserved_seating_venues = (
        Seat.objects.values("venue_id").distinct().count()
    )

    max_capacity_data = Venue.objects.aggregate(max_cap=Max("capacity"))
    max_capacity = max_capacity_data["max_cap"] or 0


    promo_percentage = Promotion.objects.filter(
        discount_type="PERCENTAGE"
    ).count()


    promo_nominal = Promotion.objects.filter(discount_type="NOMINAL").count()

    total_promo_usage = OrderPromotion.objects.count()


    context = {
        "total_users": f"{total_users:,}".replace(
            ",", "."
        ),  
        "total_events": f"{total_events:,}".replace(",", "."),
        "total_omzet": formatted_omzet,
        "active_promos": active_promos,
        "total_venues": total_venues,
        "reserved_seating_venues": reserved_seating_venues,
        "max_capacity": f"{max_capacity:,}".replace(",", "."),
        "promo_percentage": promo_percentage,
        "promo_nominal": promo_nominal,
        "total_promo_usage": total_promo_usage,
    }

    return render(request, "dashboard/dashboard_admin.html", context)
def show_profile_customer(request):
    return render(request, 'profile_customer.html')
def show_profile_organizer(request):
    return render(request, 'profile_organizer.html')