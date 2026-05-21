from django.shortcuts import render, redirect
from django.db import connection, InternalError, DatabaseError
from django.contrib import messages
import uuid

from basdut_adventure.decorators import login_required 

def execute_query(query, params=None, fetch=False):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO TikTakTuk;")
        cursor.execute(query, params)
        if fetch:
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        return None


@login_required
def show_seat(request):
    role = request.session.get('role')
    
    if role == 'Customer':
        messages.error(request, "Akses ditolak! Customer tidak memiliki izin untuk melihat Manajemen Kursi.")
        return redirect('dashboard:dashboard_customer') 

    query_seats = """
        SELECT 
            s.seat_id, 
            s.section, 
            s.row_number AS row, 
            s.seat_number AS number, 
            v.venue_name AS venue,
            v.venue_id AS venue_id,
            CASE 
                WHEN hr.seat_id IS NOT NULL THEN 'TERISI' 
                ELSE 'TERSEDIA' 
            END AS status
        FROM SEAT s
        JOIN VENUE v ON s.venue_id = v.venue_id
        LEFT JOIN HAS_RELATIONSHIP hr ON s.seat_id = hr.seat_id;
    """
    seats = execute_query(query_seats, fetch=True)
    if not seats:
        seats = []


    total_kursi = len(seats)
    tersedia = sum(1 for s in seats if s['status'] == 'TERSEDIA')
    terisi = sum(1 for s in seats if s['status'] == 'TERISI')


    venues = execute_query("SELECT venue_id, venue_name FROM VENUE;", fetch=True)

    context = {
        "seats": seats,
        "total_kursi": total_kursi,
        "tersedia": tersedia,
        "terisi": terisi,
        "venues": venues,
    }
    return render(request, 'seat.html', context)


@login_required
def seat_action(request):
    role = request.session.get('role')
    
    if role == 'Customer':
        messages.error(request, "Aksi diblokir! Customer tidak diizinkan menambah, mengubah, atau menghapus data kursi.")
        return redirect('dashboard:dashboard_customer')

    if request.method == 'POST':
        action_type = request.POST.get('action_type', 'create')
        
        try:
            if action_type == 'create':
                seat_id = str(uuid.uuid4())
                section = request.POST.get('section')
                row_number = request.POST.get('row')
                seat_number = request.POST.get('number')
                venue_id = request.POST.get('venue')
                
                query = """
                    INSERT INTO SEAT (seat_id, section, row_number, seat_number, venue_id) 
                    VALUES (%s, %s, %s, %s, %s);
                """
                execute_query(query, [seat_id, section, row_number, seat_number, venue_id])
                messages.success(request, "Kursi berhasil ditambahkan.")

            elif action_type == 'update':
                seat_id = request.POST.get('seat_id')
                section = request.POST.get('section')
                row_number = request.POST.get('row')
                seat_number = request.POST.get('number')
                venue_id = request.POST.get('venue')
                
                query = """
                    UPDATE SEAT 
                    SET section = %s, row_number = %s, seat_number = %s, venue_id = %s
                    WHERE seat_id = %s;
                """
                execute_query(query, [section, row_number, seat_number, venue_id, seat_id])
                messages.success(request, "Data kursi berhasil diperbarui.")

            elif action_type == 'delete':
                seat_id = request.POST.get('seat_id')
                query = "DELETE FROM SEAT WHERE seat_id = %s;"
                execute_query(query, [seat_id])
                messages.success(request, "Kursi berhasil dihapus.")

        except DatabaseError as e:
            # Menangkap error dari PostgreSQL dan memotong bagian "CONTEXT:"
            error_msg = str(e).split('CONTEXT:')[0].strip()
            messages.error(request, error_msg)
            
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan sistem: {str(e)}")
            
    return redirect('seat:show_seat')