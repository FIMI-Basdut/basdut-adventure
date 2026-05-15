from django.shortcuts import render, redirect
from basdut_adventure.db import get_connection
from basdut_adventure.decorators import login_required 
from django.db import connection, InternalError, DatabaseError
from basdut_adventure.db import execute_query
from django.contrib import messages

@login_required
def show_venue_list(request):
    db_user = get_db_user(request)

    query_all_cities = "SELECT DISTINCT city FROM VENUE ORDER BY city ASC"
    city_rows = execute_query(query_all_cities, fetch=True)
    all_cities = [row['city'] for row in city_rows]

    venues = get_venues(request)

    total_venue = len(venues)
    total_jenis_reserved_seating = sum(1 for v in venues if v['jenis_seating'] == "Reserved Seating")
    total_kapasitas = sum(v['capacity'] for v in venues)
        
    
    context = {
        'user': db_user,
        'venues': venues,
        'total_venue': total_venue,
        'total_jenis_reserved_seating': total_jenis_reserved_seating,
        'total_kapasitas': total_kapasitas,
        'all_cities': all_cities,
    }
    return render(request, 'venue_list_page.html', context)


# Verifikasi user_id dan (nama) role dari session dengan yang disimpan di database
# lalu mengembalikan sebuah dictionary db_user yang berisi 
# user_id, username, password, role_id, dan role_name user tersebut
def get_db_user(request):
    session_user_id = request.session.get('user_id')
    session_role = request.session.get('role')

    if not session_user_id or not session_role:
        return redirect('autentikasi:login')

    query_get_role = """
        SELECT *
        FROM USER_ACCOUNT AS ua, ROLE AS r, ACCOUNT_ROLE AS ar
        WHERE ua.user_id = ar.user_id
              and r.role_id = ar.role_id
              and ua.user_id = %s
        ORDER BY ua.user_id ASC, r.role_name ASC;
    """
    params = (session_user_id,)

    try:
        rows = execute_query(query_get_role, params, fetch=True)
        if not rows:
            messages.error(request, "Akun tidak ditemukan di database.")
            return redirect('autentikasi:login')
        
        db_user = rows[0]

        for r in rows:
            print(r)
        
        if ((str(session_user_id) == str(db_user['user_id'])) and (session_role == db_user['role_name'])):
            return db_user
        else:
            request.session.flush()
            messages.error(request, "Sesi tidak valid. Silakan login kembali.")
            return redirect('autentikasi:login')

    except Exception as e:
        print(f"Error pada show_venue_list: {e}")
        messages.error(request, "Terjadi kesalahan sistem. Silakan coba lagi nanti.")
        return redirect('autentikasi:login')

def get_venues(request):
    filter_seating = request.GET.get('seating', '')
    filter_city = request.GET.get('city', '')
    search_query = request.GET.get('search', '')
    
    query_get_venues = """
        SELECT *
        FROM VENUE
        WHERE 1=1
    """
    params = []

    if search_query:
        query_get_venues += " AND (venue_name ILIKE %s OR address ILIKE %s)"
        search_param = f"%{search_query}%"
        params.append(search_param) # nama venue
        params.append(search_param) # alamat venue

    if filter_city:
        query_get_venues += " AND city = %s"
        params.append(filter_city)
    
    if filter_seating:
        query_get_venues += " AND jenis_seating = %s"
        params.append(filter_seating)

    query_get_venues += " ORDER BY venue_name ASC;"
    rows = execute_query(query_get_venues, tuple(params), fetch=True)

    return rows
