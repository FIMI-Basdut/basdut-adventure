from django.shortcuts import render, redirect
from django.db import connection, InternalError, DatabaseError
from django.contrib import messages
import uuid

# Import decorator buatanmu
from basdut_adventure.decorators import login_required 

def execute_query(query, params=None, fetch=False):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO TikTakTuk, public;")
        cursor.execute(query, params)
        if fetch:
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        return None

@login_required
def show_ticket(request):
    role = request.session.get('role')
    user_id = request.session.get('user_id')

    query_tickets = """
        SELECT 
            t.ticket_id, 
            t.ticket_code AS code,
            e.event_id,
            e.event_title AS event,
            tc.category_name AS category,
            TO_CHAR(e.event_datetime, 'YYYY-MM-DD HH24:MI') AS date,
            tc.price,
            v.venue_name AS venue,
            o.order_id AS order,
            c.full_name AS customer,
            s.seat_id,
            s.section || ' — Baris ' || s.row_number || ', No. ' || s.seat_number AS seat_label,
            COALESCE(s.section || ' — Baris ' || s.row_number || ', No. ' || s.seat_number, 'Tanpa Kursi (Festival)') AS seat,
            o.payment_status AS status
        FROM TICKET t
        JOIN TICKET_CATEGORY tc ON t.tcategory_id = tc.category_id
        JOIN EVENT e ON tc.tevent_id = e.event_id
        JOIN VENUE v ON e.venue_id = v.venue_id
        JOIN TICKET_ORDER o ON t.torder_id = o.order_id
        JOIN CUSTOMER c ON o.customer_id = c.customer_id
        LEFT JOIN HAS_RELATIONSHIP hr ON t.ticket_id = hr.ticket_id
        LEFT JOIN SEAT s ON hr.seat_id = s.seat_id
    """
    
    params = []
    if role == 'Customer':
        query_tickets += " WHERE c.user_id = %s "
        params.append(user_id)
        
    query_tickets += " ORDER BY t.ticket_id DESC;" 
    
    tickets = execute_query(query_tickets, params, fetch=True) or []

    # Statistik (Total, Lunas, Pending)
    total_tickets = len(tickets)
    valid_tickets = sum(1 for t in tickets if t['status'] == 'Lunas')
    used_tickets = sum(1 for t in tickets if t['status'] == 'Pending') 

    context = {
        "tickets": tickets,
        "total_tickets": total_tickets,
        "valid_tickets": valid_tickets,
        "used_tickets": used_tickets,
    }

    if role != 'Customer':
        query_orders = """
            SELECT DISTINCT o.order_id, c.full_name, e.event_title, e.event_id 
            FROM TICKET_ORDER o 
            JOIN CUSTOMER c ON o.customer_id = c.customer_id
            LEFT JOIN TICKET t ON t.torder_id = o.order_id 
            LEFT JOIN TICKET_CATEGORY tc ON t.tcategory_id = tc.category_id
            LEFT JOIN EVENT e ON tc.tevent_id = e.event_id;
        """
        
        query_categories = """
            SELECT tc.category_id, tc.category_name, tc.price, tc.tevent_id AS event_id,
                   tc.quota AS kuota,
                   (SELECT COUNT(*) FROM TICKET WHERE tcategory_id = tc.category_id) AS terpakai
            FROM TICKET_CATEGORY tc;
        """

        query_seats = """
            SELECT s.seat_id, s.section, s.row_number, s.seat_number, e.event_id 
            FROM SEAT s 
            JOIN VENUE v ON s.venue_id = v.venue_id
            JOIN EVENT e ON e.venue_id = v.venue_id
            WHERE s.seat_id NOT IN (
                SELECT hr.seat_id 
                FROM HAS_RELATIONSHIP hr
                JOIN TICKET t ON hr.ticket_id = t.ticket_id
                JOIN TICKET_CATEGORY tc ON t.tcategory_id = tc.category_id
                WHERE tc.tevent_id = e.event_id
            );
        """
        
        context['orders'] = execute_query(query_orders, fetch=True) or []
        context['categories'] = execute_query(query_categories, fetch=True) or []
        context['seats'] = execute_query(query_seats, fetch=True) or []
        context['role'] = role
        return render(request, 'ticket.html', context)

    else:
        return render(request, 'ticket_customer.html', context)


@login_required
def ticket_action(request):
    role = request.session.get('role')
    
    if role == 'Customer':
        messages.error(request, "Aksi diblokir! Customer tidak diizinkan memodifikasi data tiket.")
        return redirect('ticket:show_ticket')
    
    if role == 'Organizer':
        messages.error(request, "Aksi diblokir! Organizer tidak diizinkan memodifikasi data tiket.")
        return redirect('ticket:show_ticket')

    if request.method == 'POST':
        action_type = request.POST.get('action_type')
        
        try:
            if action_type == 'create':
                ticket_id = str(uuid.uuid4())
                ticket_code = f"TTK-{str(uuid.uuid4())[:8].upper()}" 
                tcategory_id = request.POST.get('category')
                torder_id = request.POST.get('order')
                seat_id = request.POST.get('seat')
                
                query_ticket = "INSERT INTO TICKET (ticket_id, ticket_code, tcategory_id, torder_id) VALUES (%s, %s, %s, %s);"
                execute_query(query_ticket, [ticket_id, ticket_code, tcategory_id, torder_id])

                if seat_id:
                    query_rel = "INSERT INTO HAS_RELATIONSHIP (seat_id, ticket_id) VALUES (%s, %s);"
                    execute_query(query_rel, [seat_id, ticket_id])

                messages.success(request, f"Tiket {ticket_code} berhasil dibuat!")

            elif action_type == 'update':
                ticket_id = request.POST.get('ticket_id')
                new_status = request.POST.get('status')
                new_seat_id = request.POST.get('seat')
                
                # 1. Update Status Pembayaran (TICKET_ORDER)
                query_update = """
                    UPDATE TICKET_ORDER 
                    SET payment_status = %s 
                    WHERE order_id = (SELECT torder_id FROM TICKET WHERE ticket_id = %s);
                """
                execute_query(query_update, [new_status, ticket_id])

                # 2. Update Kursi (HAS_RELATIONSHIP)
                execute_query("DELETE FROM HAS_RELATIONSHIP WHERE ticket_id = %s;", [ticket_id])
                
                if new_seat_id:
                    execute_query("INSERT INTO HAS_RELATIONSHIP (seat_id, ticket_id) VALUES (%s, %s);", [new_seat_id, ticket_id])

                messages.success(request, "Tiket berhasil diperbarui.")

            elif action_type == 'delete':
                ticket_id = request.POST.get('ticket_id')
                execute_query("DELETE FROM TICKET WHERE ticket_id = %s;", [ticket_id])
                messages.success(request, "Tiket berhasil dihapus.")

        except DatabaseError as e:
            error_msg = str(e).split('CONTEXT:')[0].strip()
            messages.error(request, error_msg)
            
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan sistem: {str(e)}")
            
    return redirect('ticket:show_ticket')