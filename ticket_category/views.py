import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Max
from django.utils import timezone
from basdut_adventure.db import get_connection
from basdut_adventure.decorators import login_required

@login_required
def daftar_tiket_kategori(request):
    role= request.session.get('role')
    if role != 'Customer' and role != 'Organizer':
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
                SELECT TC.category_id,TC.category_name,E.event_title,TC.price,TC.quota
                FROM ticket_category TC
                JOIN event E ON TC.tevent_id = E.event_id
                ORDER BY E.event_title
                """
            )
            rows= cursor.fetchall()
            categories = []
            for row in rows:
                category={
                    'category_id': row[0],
                    'category_name': row[1],
                    'event_name': row[2],
                    'price': row[3],
                    'quota': row[4]
                }
                categories.append(category)
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM ticket_category
                """
            )
            row = cursor.fetchone()
            total_categories = row[0] if row else 0
            cursor.execute(
                """
                SELECT SUM(quota)
                FROM ticket_category
                """
            )
            row = cursor.fetchone()
            total_quota = row[0] if row else 0
            cursor.execute(
                """
                SELECT MAX(price)
                FROM ticket_category
                """
            )
            row = cursor.fetchone()
            highest_price = row[0] if row else 0
    context = {
        'categories': categories,
        'total_categories': total_categories,
        'total_quota': total_quota,
        'highest_price': highest_price,
    }
    return render(request, 'tiket_kategori.html', context)

@login_required
def daftar_tiket_kategori_admin(request):
    role = request.session.get('role')
    if role != 'Admin':
        return redirect('main:mantap')
    now = timezone.now()
    today = now.date()
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        category_name = request.POST.get('category_name', '').strip()
        quota = request.POST.get('quota')
        price = request.POST.get('price')

        if not all([event_id, category_name, quota, price]):
            messages.error(request, 'Semua input wajib diisi!')
        elif int(quota) <= 0:
            messages.error(request, 'Kuota harus lebih dari 0.')
        elif float(price) < 0:
            messages.error(request, 'Harga tidak boleh negatif.')
        else:
            id_category=str(uuid.uuid4())
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SET search_path TO tiktaktuk, public
                        """
                    )
                    cursor.execute(
                        """
                        INSERT INTO TICKET_CATEGORY(category_id,category_name,price,quota,tevent_id)
                        VALUES (%s,%s,%s,%s,%s)
                        """,
                        [id_category, category_name, price, quota, event_id]
                    )
            messages.success(request, 'Daftar ticket_category diperbarui.')
        
        return redirect('ticket_category:daftar_tiket_kategori_admin')
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SET search_path TO tiktaktuk, public
                """
            )
            cursor.execute(
                """
                SELECT TC.category_id,TC.category_name,E.event_title,TC.price,TC.quota
                FROM ticket_category TC
                JOIN event E ON TC.tevent_id = E.event_id
                ORDER BY E.event_title
                """
            )
            rows= cursor.fetchall()
            categories = []
            for row in rows:
                category={
                    'category_id': row[0],
                    'category_name': row[1],
                    'event_name': row[2],
                    'price': row[3],
                    'quota': row[4]
                }
                categories.append(category)
            cursor.execute(
                """
                SELECT E.event_id,E.event_title
                FROM event E
                WHERE E.event_datetime > %s
                """,
                [today]
            )
            rows = cursor.fetchall()
            events = []
            for row in rows:
                event = {
                    'event_id': row[0],
                    'event_title': row[1]
                }
                events.append(event)
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM ticket_category
                """
            )
            row = cursor.fetchone()
            total_categories = row[0] if row else 0
            cursor.execute(
                """
                SELECT SUM(quota)
                FROM ticket_category
                """
            )
            row = cursor.fetchone()
            total_quota = row[0] if row else 0
            cursor.execute(
                """
                SELECT MAX(price)
                FROM ticket_category
                """
            )
            row = cursor.fetchone()
            highest_price = row[0] if row else 0
    
    context = {
        'categories': categories,
        'events': events, 
        'total_categories': total_categories,
        'total_quota': total_quota,
        'highest_price': highest_price,
    }
    return render(request, 'tiket_kategori_admin.html', context)

@login_required
def edit_tiket_kategori(request, id):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        category_name = request.POST.get('category_name', '').strip()
        quota = request.POST.get('quota')
        price = request.POST.get('price')

        if not all([event_id, category_name, quota, price]):
            messages.error(request, 'Semua input wajib diisi!')
        elif int(quota) <= 0:
            messages.error(request, 'Kuota harus lebih dari 0.')
        elif float(price) < 0:
            messages.error(request, 'Harga tidak boleh negatif.')
        else:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SET search_path TO tiktaktuk, public
                        """
                    )
                    cursor.execute(
                        """
                        UPDATE TICKET_CATEGORY
                        SET category_name = %s, price = %s, quota = %s, tevent_id = %s
                        WHERE category_id = %s
                        """,
                        [category_name, price, quota, event_id, id]
                    )
            messages.success(request, 'Daftar ticket_category diperbarui.')

    return redirect('ticket_category:daftar_tiket_kategori_admin')

@login_required
def hapus_tiket_kategori(request, id):
    if request.method == 'POST':
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SET search_path TO tiktaktuk, public
                    """
                )
                cursor.execute(
                    """
                    DELETE FROM TICKET_CATEGORY
                    WHERE category_id = %s
                    """,
                    [id]
                )
        messages.success(request, 'Kategori tiket berhasil dihapus.')
    return redirect('ticket_category:daftar_tiket_kategori_admin')