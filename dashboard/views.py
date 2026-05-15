from datetime import date
from django.db.models import Count, Max, Sum,DecimalField, ExpressionWrapper, F
from django.shortcuts import render,redirect
from django.utils import timezone
from psycopg import cursor
from basdut_adventure.db import get_connection
from basdut_adventure.decorators import login_required






# Create your views here.

@login_required
def show_dashboard_customer(request):
    role= request.session.get('role')
    if role != 'Customer':
        return redirect('main:mantap')
    now = timezone.now()
    today = now.date()
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SET search_path TO tiktaktuk, public
                """
            )
            cursor.execute(
                """
                SELECT full_name
                FROM CUSTOMER
                WHERE user_id = %s
                """,
                [request.session.get('user_id')]
            )
            row = cursor.fetchone()
            customer_name = row[0]
            cursor.execute(
                """
                SELECT customer_id
                FROM CUSTOMER
                WHERE user_id = %s
                """,
                [request.session.get('user_id')]
            )
            row= cursor.fetchone()
            customer_id =  row[0]
            cursor.execute(
                """
                SELECT COALESCE(COUNT(TICKET.ticket_id), 0) AS total
                FROM TICKET
                JOIN TICKET_ORDER ON TICKET.torder_id = TICKET_ORDER.order_id
                JOIN TICKET_CATEGORY ON TICKET.tcategory_id = TICKET_CATEGORY.category_id
                JOIN EVENT ON TICKET_CATEGORY.tevent_id = EVENT.event_id
                WHERE TICKET_ORDER.customer_id = %s AND EVENT.event_datetime > %s
                """,
                [customer_id,now]
            )
            row = cursor.fetchone()
            tiket_aktif = row[0]
            cursor.execute(
                """
                SELECT COUNT(DISTINCT tevent_id) AS count
                FROM TICKET
                JOIN TICKET_ORDER ON TICKET.torder_id = TICKET_ORDER.order_id
                JOIN TICKET_CATEGORY ON TICKET.tcategory_id = TICKET_CATEGORY.category_id
                WHERE TICKET_ORDER.customer_id = %s
                """,
                [customer_id]
            )
            row = cursor.fetchone()
            acara_diikuti = row[0]
            cursor.execute(
                """
                SELECT COUNT(*) AS banyak_promo
                FROM PROMOTION
                WHERE end_date > %s AND usage_limit > 0
                """,
                [today]
            )
            row = cursor.fetchone()
            banyak_promo = row[0]
            cursor.execute(
                """
                    SELECT COALESCE(SUM(TICKET_ORDER.total_amount), 0) AS total_belanja
                    FROM TICKET_ORDER
                    WHERE TICKET_ORDER.customer_id = %s
                """,
                [customer_id]
            )
            row= cursor.fetchone()
            total_belanja_raw= row[0]
            cursor.execute(
                """
                    SELECT EVENT.event_title,TICKET_CATEGORY.category_name, EVENT.event_datetime,VENUE.venue_name
                    FROM TICKET_CATEGORY
                    JOIN EVENT ON TICKET_CATEGORY.tevent_id = EVENT.event_id
                    JOIN VENUE ON EVENT.venue_id = VENUE.venue_id
                    WHERE EVENT.event_datetime > %s
                    ORDER BY EVENT.event_datetime ASC
                """,
                [now]
            )
            rows = cursor.fetchall()
            ticket_mendatang_list = []
            for row in rows:
                ticket={
                    "event_title": row[0],
                    "category_name": row[1],
                    "event_datetime": row[2],
                    "venue_name": row[3],
                }
                ticket_mendatang_list.append(ticket)
            cursor.execute(
                """
                    SELECT COUNT(*) AS sisa_acara_count
                    FROM EVENT
                    WHERE event_datetime > %s
                """,
                [now]
            )
            row = cursor.fetchone()
            sisa_acara_count = row[0]

    def format_rupiah(amount):
        if amount >= 1_000_000_000:
            return f"Rp {amount / 1_000_000_000:.1f}M"
        elif amount >= 1_000_000:
            return f"Rp {amount / 1_000_000:.1f}Jt"
        elif amount > 0:
            return f"Rp {amount:,.0f}".replace(",", ".")
        return "Rp 0"

    total_belanjaFormatted = format_rupiah(total_belanja_raw)


    context = {
        "customer_name": customer_name,
        "sisa_acara_count": sisa_acara_count,
        "tiket_aktif": f"{int(tiket_aktif):,}".replace(",", "."),
        "acara_diikuti": acara_diikuti,
        "banyak_promo": banyak_promo,
        "total_belanja": total_belanjaFormatted,
        "tiket_mendatang_list": ticket_mendatang_list,
    }

    return render(request, "dashboard_customer.html", context)
@login_required
def show_dashboard_organizer(request):
    role= request.session.get('role')
    if role != 'Organizer':
        return redirect('main:mantap')
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SET search_path TO tiktaktuk, public
                """
            )
            cursor.execute(
                """
                SELECT organizer_name
                FROM ORGANIZER
                WHERE user_id = %s
                """,
                [request.session.get('user_id')]
            )
            row = cursor.fetchone()
            organizer_name = row[0]
            cursor.execute(
                """
                SELECT organizer_id
                FROM ORGANIZER
                WHERE user_id = %s
                """,
                [request.session.get('user_id')]
            )
            row = cursor.fetchone()
            organizer_id = row[0]
            cursor.execute(
                """
                SELECT COUNT(*) AS total_events
                FROM EVENT
                WHERE organizer_id = %s
                """,
                [organizer_id]
            )
            row = cursor.fetchone()
            total_events_dikelola = row[0]
            cursor.execute(
                """
                SELECT COALESCE(COUNT(TICKET.ticket_id), 0) AS tiket_terjual
                FROM TICKET
                JOIN TICKET_CATEGORY ON TICKET.tcategory_id = TICKET_CATEGORY.category_id
                JOIN EVENT ON TICKET_CATEGORY.tevent_id = EVENT.event_id
                WHERE EVENT.organizer_id = %s
                """,
                [organizer_id]
            )
            row = cursor.fetchone()
            tiket_terjual = row[0]
            cursor.execute(
                """
                SELECT COALESCE(SUM(total_amount), 0) AS revenue
                FROM TICKET_ORDER
                WHERE order_id IN (
                    -- Mencari ID Pesanan yang unik (DISTINCT) untuk acara organizer ini
                    SELECT DISTINCT TICKET.torder_id
                    FROM TICKET
                    JOIN TICKET_CATEGORY ON TICKET.tcategory_id = TICKET_CATEGORY.category_id
                    JOIN EVENT ON TICKET_CATEGORY.tevent_id = EVENT.event_id
                    WHERE EVENT.organizer_id = %s 
                    AND EXTRACT(YEAR FROM EVENT.event_datetime) = %s 
                    AND EXTRACT(MONTH FROM EVENT.event_datetime) = %s
                )
                """,
                [organizer_id, timezone.now().year, timezone.now().month]
            )
            row = cursor.fetchone()
            revenue_raw = row[0]
            cursor.execute(
                """
                SELECT COALESCE(COUNT(DISTINCT VENUE.venue_id), 0) AS venue_mitra
                FROM VENUE
                JOIN EVENT ON VENUE.venue_id = EVENT.venue_id
                WHERE EVENT.organizer_id = %s
                """,
                [organizer_id]
            )
            row = cursor.fetchone()
            venue_mitra = row[0]
            cursor.execute(
                """
                SELECT 
                    e.event_title, 
                    COALESCE(t.terjual, 0) AS tiket_terjual,
                    COALESCE(q.total_quota, 0) AS total_tiket, 
                    v.venue_name
                FROM EVENT e
                JOIN VENUE v ON e.venue_id = v.venue_id
                LEFT JOIN (
                    SELECT tevent_id, SUM(quota) AS total_quota 
                    FROM TICKET_CATEGORY 
                    GROUP BY tevent_id
                ) q ON e.event_id = q.tevent_id
                LEFT JOIN (
                    SELECT tc.tevent_id, COUNT(t.ticket_id) AS terjual 
                    FROM TICKET t 
                    JOIN TICKET_CATEGORY tc ON t.tcategory_id = tc.category_id 
                    GROUP BY tc.tevent_id
                ) t ON e.event_id = t.tevent_id
                WHERE e.organizer_id = %s
                ORDER BY e.event_datetime ASC
                """,
                [organizer_id]
            )
            rows = cursor.fetchall()
            event_list = []
            for row in rows:
                event ={
                    "event_title": row[0],
                    "tiket_terjual": row[1]/row[2]*100 if row[2] > 0 else 0,
                    "venue_name": row[3],
                }
                event_list.append(event)
    
    def format_revenue(amount):
        if amount >= 1_000_000_000:
            return f"Rp {amount / 1_000_000_000:.1f}M"
        elif amount >= 1_000_000:
            return f"Rp {amount / 1_000_000:.1f}Jt"
        elif amount > 0:
            return f"Rp {amount:,.0f}".replace(",", ".")
        return "Rp 0"
    revenue = format_revenue(revenue_raw)
    context = {
        "organizer_name": organizer_name,
        "total_events_dikelola": f"{total_events_dikelola:,}".replace(",", "."),
        "tiket_terjual": f"{tiket_terjual:,}".replace(",", "."),
        "revenue": revenue,
        "venue_mitra": f"{venue_mitra:,}".replace(",", "."),
        "event_list": event_list,
    }
    return render(request, 'dashboard_organizer.html', context)
@login_required
def show_dashboard_admin(request):
    role= request.session.get('role')
    if role != 'Admin':
        return redirect('main:mantap')
    now = timezone.now()
    today = now.date()
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SET search_path TO tiktaktuk, public
                """
            )
            cursor.execute(
                """
                SELECT COUNT(*) AS total_users
                FROM User_Account
                """
            )
            row = cursor.fetchone()
            total_users = row[0]
            cursor.execute(
                """
                SELECT COUNT(*) AS total_events
                FROM EVENT
                WHERE EXTRACT(YEAR FROM event_datetime) = %s AND EXTRACT(MONTH FROM event_datetime) = %s
                """,
                [now.year, now.month]
            )
            row = cursor.fetchone()
            total_events = row[0]
            cursor.execute(
                """
                SELECT COALESCE(SUM(TICKET_ORDER.total_amount), 0) AS total_omzet
                FROM TICKET_ORDER
                """
            )
            row = cursor.fetchone()
            total_omzet = row[0]
            cursor.execute(
                """
                SELECT COUNT(*) AS active_promos
                FROM PROMOTION
                WHERE end_date > %s AND usage_limit > 0
                """,
                [today]
            )
            row = cursor.fetchone()
            active_promos = row[0]
            cursor.execute(
                """
                SELECT COUNT(*) AS total_venues
                FROM VENUE
                """
            )
            row = cursor.fetchone()
            total_venues = row[0]
            cursor.execute(
                """
                SELECT COUNT(DISTINCT venue_id) AS reserved_seating_venues
                FROM SEAT
                """
            )
            row = cursor.fetchone()
            reserved_seating_venues = row[0]
            cursor.execute(
                """
                SELECT COALESCE(MAX(capacity), 0) AS max_capacity
                FROM VENUE
                """
            )
            row = cursor.fetchone()
            max_capacity = row[0]
            cursor.execute(
                """
                SELECT COUNT(*) AS promo_percentage
                FROM PROMOTION
                WHERE discount_type = 'PERCENTAGE'
                """
            )
            row = cursor.fetchone()
            promo_percentage = row[0]
            cursor.execute(
                """
                SELECT COUNT(*) AS promo_nominal
                FROM PROMOTION
                WHERE discount_type = 'NOMINAL'
                """
            )
            row = cursor.fetchone()
            promo_nominal = row[0]
            cursor.execute(
                """
                SELECT COUNT(*) AS total_promo_usage
                FROM ORDER_PROMOTION
                """
            )
            row = cursor.fetchone()
            total_promo_usage = row[0]


    def format_omzet(amount):
        if amount >= 1_000_000_000:
            return f"Rp {amount / 1_000_000_000:.1f}M"
        elif amount >= 1_000_000:
            return f"Rp {amount / 1_000_000:.1f}Jt"
        elif amount > 0:
            return f"Rp {amount:,.0f}".replace(",", ".")
        return "Rp 0"

    formatted_omzet = format_omzet(total_omzet)



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
@login_required
def show_profile_customer(request):
    role = request.session.get('role')
    user_id = request.session.get('user_id')

    if role != 'Customer':
        return redirect('main:mantap')

    context = {}

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            context['error'] = 'Password baru dan konfirmasi password tidak cocok.'
        else:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SET search_path TO tiktaktuk, public
                        """
                    )
                    cursor.execute(
                        "SELECT password FROM USER_ACCOUNT WHERE user_id = %s",
                        [user_id]
                    )
                    row = cursor.fetchone()
                    
                    if row and row[0] != old_password:
                        context['error'] = 'Password lama salah.'
                    else:
                        cursor.execute(
                            """
                            UPDATE USER_ACCOUNT
                            SET password = %s
                            WHERE user_id = %s
                            """,
                            [new_password, user_id]
                        )
                        context['success'] = 'Password berhasil diubah!'

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                        """
                        SET search_path TO tiktaktuk, public
                        """
            )
            cursor.execute(
                """
                SELECT CUSTOMER.full_name, CUSTOMER.phone_number, USER_ACCOUNT.username
                FROM CUSTOMER
                JOIN USER_ACCOUNT ON CUSTOMER.user_id = USER_ACCOUNT.user_id
                WHERE CUSTOMER.user_id = %s
                """,
                [user_id]
            )
            row = cursor.fetchone()
            if row:
                customer = {
                    "full_name": row[0],
                    "phone_number": row[1],
                    "username": row[2],
                }
                context['customer'] = customer

    return render(request, 'profile_customer.html', context)
@login_required
def show_profile_organizer(request):
    role= request.session.get('role')
    user_id = request.session.get('user_id')
    if role != 'Organizer':
        return redirect('main:mantap')
    context = {}

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SET search_path TO tiktaktuk, public
                    """
                )
                cursor.execute(
                    "SELECT password FROM USER_ACCOUNT WHERE user_id = %s",
                    [user_id]
                )
                row = cursor.fetchone()
                
                if row and row[0] != old_password or new_password != confirm_password:
                    context['error'] = 'Password lama atau konfirmasi password salah.'
                else:
                    cursor.execute(
                        """
                        UPDATE USER_ACCOUNT
                        SET password = %s
                        WHERE user_id = %s
                        """,
                        [new_password, user_id]
                    )
                    context['success'] = 'Password berhasil diubah!'
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SET search_path TO tiktaktuk, public
                """
            )
            cursor.execute(
                """
                SELECT ORGANIZER.organizer_name, ORGANIZER.contact_email, USER_ACCOUNT.username
                FROM ORGANIZER
                JOIN USER_ACCOUNT ON ORGANIZER.user_id = USER_ACCOUNT.user_id
                WHERE ORGANIZER.user_id = %s
                """,
                [user_id]
            )
            row = cursor.fetchone()
            organizer={
                "organizer_name": row[0],
                "contact_email": row[1],
                "username": row[2],
            }
            context['organizer'] = organizer
    return render(request, 'profile_organizer.html', context)