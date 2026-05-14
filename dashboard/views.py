from datetime import date
from django.db.models import Count, Max, Sum,DecimalField, ExpressionWrapper, F
from django.shortcuts import render
from django.utils import timezone
from basdut_adventure.db import get_connection

from .models import (
    Event,
    OrderPromotion,
    Promotion,
    Seat,
    Ticket,
    UserAccount,
    Venue,
    Customer,
    TicketOrder,
    TicketCategory
)




# Create your views here.

def show_dashboard_customer(request):
    # if request.user.is_authenticated:
    #     customer = Customer.objects.filter(user=request.user).first()
    customer = Customer.objects.select_related("user").first()

    if not customer:
        return render(request, "dashboard_customer.html", {"customer_name": "Pengguna Dummy"})

    customer_name = customer.full_name
    now = timezone.now()
    today = now.date()

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT COALESCE(SUM(total_amount), 0) AS total
                FROM TICKET_ORDER
                WHERE customer_id = %s
                """,
                [customer.customer_id]
            )
            row = cursor.fetchone()
            tiket_aktif = row[0] if row else 0
    tiket_aktif_data = TicketOrder.objects.filter(customer=customer).aggregate(
        total=Sum("total_amount")
    )
    tiket_aktif = tiket_aktif_data["total"] or 0

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(DISTINCT tevent_id) AS count
                FROM TICKET
                JOIN TICKET_ORDER ON TICKET.torder_id = TICKET_ORDER.order_id
                JOIN TICKET_CATEGORY ON TICKET.tcategory_id = TICKET_CATEGORY.category_id
                WHERE TICKET_ORDER.customer_id = %s
                """,
                [customer.customer_id]
            )
            row = cursor.fetchone()
    acara_diikuti = row[0] if row else 0

    acara_diikuti = (
        Ticket.objects.filter(torder__customer=customer)
        .values("tcategory__tevent_id")
        .distinct()
        .count()
    )

    kode_promo = Promotion.objects.filter(end_date__gt=today, usage_limit__gt=0).count()


    perkalian_expr = ExpressionWrapper(
        F("torder__total_amount") * F("tcategory__price"), output_field=DecimalField()
    )
    total_belanja_data = Ticket.objects.filter(torder__customer=customer).aggregate(
        grand_total=Sum(perkalian_expr)
    )
    total_belanja_raw = total_belanja_data["grand_total"] or 0


    def format_rupiah(amount):
        if amount >= 1_000_000_000:
            return f"Rp {amount / 1_000_000_000:.1f}M"
        elif amount >= 1_000_000:
            return f"Rp {amount / 1_000_000:.1f}Jt"
        elif amount > 0:
            return f"Rp {amount:,.0f}".replace(",", ".")
        return "Rp 0"

    total_belanjaFormatted = format_rupiah(total_belanja_raw)



    tiket_mendatang_list = TicketCategory.objects.filter(
        tevent__event_datetime__gt=now
    ).select_related(
        "tevent", "tevent__venue"
    ).order_by("tevent__event_datetime", "price")

    sisa_acara_count = Event.objects.filter(event_datetime__gt=now).count()

    context = {
        "customer_name": customer_name,
        "sisa_acara_count": sisa_acara_count,
        "tiket_aktif": f"{int(tiket_aktif):,}".replace(",", "."),
        "acara_diikuti": acara_diikuti,
        "kode_promo": kode_promo,
        "total_belanja": total_belanjaFormatted,
        "tiket_mendatang_list": tiket_mendatang_list,
    }

    return render(request, "dashboard_customer.html", context)
def show_dashboard_organizer(request):
    return render(request, 'dashboard_organizer.html')
def show_dashboard_admin(request):

    total_users = UserAccount.objects.count()

    now = timezone.now()

    total_events = Event.objects.filter(
        event_datetime__year=now.year,
        event_datetime__month=now.month
    ).count()


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

    return render(request, "dashboard_admin.html", context)
def show_profile_customer(request):
    return render(request, 'profile_customer.html')
def show_profile_organizer(request):
    return render(request, 'profile_organizer.html')