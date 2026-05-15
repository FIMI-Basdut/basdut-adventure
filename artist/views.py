import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from basdut_adventure.db import get_connection
from basdut_adventure.decorators import login_required

# VIEWS UNTUK NON-ADMIN (R - Artist)
@login_required
def daftar_artis(request):
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
                SELECT artist_id, artist_name, genre
                FROM ARTIST
                ORDER BY artist_name ASC
                """
            )
            rows= cursor.fetchall()
            artists = []
            for row in rows:
                artist={
                    'artist_id': row[0],
                    'name': row[1],
                    'genre': row[2]
                }
                artists.append(artist)
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM ARTIST
                """
            )
            row = cursor.fetchone()
            total_artis = row[0] if row else 0
            cursor.execute(
                """
                SELECT COUNT(DISTINCT genre)
                FROM ARTIST
                WHERE genre IS NOT NULL OR genre != ''
                """
            )
            row = cursor.fetchone()
            total_genre = row[0] if row else 0
            cursor.execute(
                """
                SELECT COUNT(DISTINCT ARTIST.artist_id)
                FROM ARTIST
                JOIN EVENT_ARTIST EA ON ARTIST.artist_id = EA.artist_id
                """
            )
            row = cursor.fetchone()
            total_artis_terlibat = row[0] if row else 0
    context = {
        'artists': artists,
        'total_artis': total_artis,
        'total_genre': total_genre,
        'total_artis_terlibat': total_artis_terlibat
    }
    return render(request, 'daftar_artis.html', context)


# VIEWS UNTUK ADMIN (CRUD - Artist)
@login_required
def daftar_artis_admin(request):
    role = request.session.get('role')
    if role != 'Admin':
        return redirect('main:mantap')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        genre = request.POST.get('genre', '').strip()

        if not name:
            messages.error(request, 'Nama wajib diisi.')
        else:
            id_artist = str(uuid.uuid4())
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SET search_path TO tiktaktuk, public
                        """
                    )
                    if genre!='':
                        cursor.execute(
                            """
                            INSERT INTO ARTIST(artist_id, artist_name, genre)
                            VALUES (%s,%s,%s)
                            """,
                            [id_artist, name, genre]
                        )
                    else:
                        cursor.execute(
                            """
                            INSERT INTO ARTIST(artist_id, artist_name)
                            VALUES (%s,%s)
                            """,
                            [id_artist, name]
                        )
            messages.success(request, 'Daftar artis diperbarui.')
        
        return redirect('artist:daftar_artis_admin') 
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SET search_path TO tiktaktuk, public
                """
            )
            cursor.execute(
                """
                SELECT artist_id, artist_name, genre
                FROM ARTIST
                ORDER BY artist_name ASC
                """
            )
            rows= cursor.fetchall()
            artists = []
            for row in rows:
                artist={
                    'artist_id': row[0],
                    'name': row[1],
                    'genre': row[2]
                }
                artists.append(artist)
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM ARTIST
                """
            )
            row = cursor.fetchone()
            total_artis = row[0] if row else 0
            cursor.execute(
                """
                SELECT COUNT(DISTINCT genre)
                FROM ARTIST
                WHERE genre IS NOT NULL OR genre !=''
                """
            )
            row = cursor.fetchone()
            total_genre = row[0] if row else 0
            cursor.execute(
                """
                SELECT COUNT(DISTINCT ARTIST.artist_id)
                FROM ARTIST
                JOIN EVENT_ARTIST EA ON ARTIST.artist_id = EA.artist_id
                """
            )
            row = cursor.fetchone()
            total_artis_terlibat = row[0] if row else 0
    context = {
        'artists': artists,
        'total_artis': total_artis,
        'total_genre': total_genre,
        'total_artis_terlibat': total_artis_terlibat
    }
    return render(request, 'daftar_artis_admin.html', context)

@login_required
def edit_artis(request, id):
    role = request.session.get('role')
    if role != 'Admin':
        return redirect('main:mantap')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        genre = request.POST.get('genre', '').strip()

        if not name:
            messages.error(request, 'Nama wajib diisi.')
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
                        UPDATE ARTIST
                        SET artist_name = %s, genre = %s
                        WHERE artist_id = %s
                        """,
                        [name, genre, id]
                    )
            messages.success(request, 'Daftar artis diperbarui.')
            
    return redirect('artist:daftar_artis_admin')

@login_required
def hapus_artis(request, id):
    role = request.session.get('role')
    if role != 'Admin':
        return redirect('main:mantap')
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
                    DELETE FROM ARTIST
                    WHERE artist_id = %s
                    """,
                    [id]
                )
        messages.success(request, 'Artis berhasil dihapus.')
        
    return redirect('artist:daftar_artis_admin')