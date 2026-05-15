from django.shortcuts import render, redirect
from basdut_adventure.db import get_connection
from basdut_adventure.decorators import login_required 
from django.db import connection, InternalError, DatabaseError
from basdut_adventure.db import execute_query
from django.contrib import messages

@login_required
def show_venue_list(request):
    db_user = get_db_user(request)
    
    context = {
        'user': db_user,
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
              and ua.user_id = %s;
    """
    params = (session_user_id,)

    try:
        rows = execute_query(query_get_role, params, fetch=True)
        if not rows:
            messages.error(request, "Akun tidak ditemukan di database.")
            return redirect('autentikasi:login')
        
        for r in rows:
            print(r)
        
        db_user = rows[0]
        
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

