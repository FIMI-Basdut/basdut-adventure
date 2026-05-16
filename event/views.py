import uuid

from django.shortcuts import render, redirect
from basdut_adventure.decorators import login_required 
from basdut_adventure.db import execute_query
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
def show_event_list(request):
    events = get_events(request)
    venues = get_venues(request)
    artists = get_artist(request)
    organizers = get_organizers(request)

    context = {
        'events': events,
        'venues': venues,
        'artists': artists,
        'organizers': organizers,
    }

    return render(request, "event_list_page.html", context)
    
def get_events(request):
    filter_artist = request.GET.get('artist', '')
    filter_venue = request.GET.get('venue', '')
    search_query = request.GET.get('search', '')

    query_get_event = """
        SELECT e.event_title, TO_CHAR(e.event_datetime, 'YYYY-MM-DD HH24:MI') as event_datetime, e.emoji, 
                v.venue_name, v.city,
                ARRAY_AGG(DISTINCT a.artist_name) AS artists,
                ARRAY_AGG(DISTINCT tc.category_name) AS ticket_categories,
                TO_CHAR(MIN(tc.price), 'FM999,999,999') AS lowest_price
        FROM EVENT e
        JOIN VENUE v ON e.venue_id = v.venue_id
        JOIN EVENT_ARTIST ea ON e.event_id = ea.event_id
        JOIN ARTIST a ON ea.artist_id = a.artist_id
        JOIN TICKET_CATEGORY tc ON e.event_id = tc.tevent_id
        WHERE 1=1
        
    """
    params = []

    if search_query:
        query_get_event += """ 
            AND (e.event_title ILIKE %s OR e.event_id IN (
                SELECT ea2.event_id 
                FROM EVENT_ARTIST ea2 
                JOIN ARTIST a2 ON ea2.artist_id = a2.artist_id 
                WHERE a2.artist_name ILIKE %s
            )) 
        """
        search_param = f"%{search_query}%"
        params.append(search_param) # judul event
        params.append(search_param) # nama artis

    if filter_artist:
        query_get_event += """ 
            AND e.event_id IN (
                SELECT ea3.event_id 
                FROM EVENT_ARTIST ea3 
                JOIN ARTIST a3 ON ea3.artist_id = a3.artist_id 
                WHERE a3.artist_name = %s
            ) 
        """
        params.append(filter_artist)
    
    if filter_venue:
        query_get_event += " AND v.venue_name = %s"
        params.append(filter_venue)

    query_get_event += """ GROUP BY event_title, e.event_datetime, v.venue_name, v.city, e.emoji
                            ORDER BY e.event_title ASC; """

    rows = execute_query(query_get_event, tuple(params), fetch=True)

    return rows

def get_venues(request): 
    query_get_venues = """
        SELECT venue_id, venue_name
        FROM VENUE
        ORDER BY venue_name ASC;
    """
    params = []

    rows = execute_query(query_get_venues, tuple(params), fetch=True)

    return rows

def get_artist(request):
    query_get_artist = """
        SELECT artist_id, artist_name
        FROM ARTIST
        ORDER BY artist_name ASC;
    """
    params = []

    rows = execute_query(query_get_artist, tuple(params), fetch=True)

    return rows

def get_organizers(request):
    query_get_organizer = """
        SELECT organizer_id, organizer_name
        FROM ORGANIZER
        ORDER BY organizer_name ASC;
    """
    params = []

    rows = execute_query(query_get_organizer, tuple(params), fetch=True)

    return rows

def add_event(request):
    if request.method == 'POST':
        print("masuk ke fungsi add_event()")

        try: 
            event_id = str(uuid.uuid4())
            event_title = request.POST.get("event_title") 
            event_date = request.POST.get("event_date") 
            event_time = request.POST.get("event_time")
            event_datetime = f"{event_date} {event_time}:00" 
            event_emoji = request.POST.get("event_emoji")
            event_description = request.POST.get("event_description")

            venue_id = request.POST.get("venue_id") 
            organizer_id = request.POST.get("organizer_id")

            query_event = """
                INSERT INTO EVENT (event_id, event_datetime, event_title, venue_id, organizer_id, emoji, event_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params_event = (event_id, event_datetime, event_title, venue_id, organizer_id, event_emoji, event_description)
            execute_query(query_event, params_event, fetch=False)

            artist_ids = request.POST.getlist("artist_ids")
            if artist_ids:
                for artist_id in artist_ids:
                    custom_role = request.POST.get(f"role_{artist_id}")
                    
                    if not custom_role or custom_role.strip() == "":
                        custom_role = "Performer"
                        
                    query_ea = "INSERT INTO EVENT_ARTIST (event_id, artist_id, role) VALUES (%s, %s, %s)"
                    execute_query(query_ea, (event_id, artist_id, custom_role), fetch=False)

            categories = request.POST.getlist("ticket_category[]")
            prices = request.POST.getlist("ticket_price[]")
            quotas = request.POST.getlist("ticket_quota[]")

            for cat_name, price, quota in zip(categories, prices, quotas):
                cat_id = str(uuid.uuid4())
                query_tc = """
                    INSERT INTO TICKET_CATEGORY (category_id, category_name, quota, price, tevent_id)
                    VALUES (%s, %s, %s, %s, %s)
                """
                execute_query(query_tc, (cat_id, cat_name, int(quota), float(price), event_id), fetch=False)

            return JsonResponse({"status": "success", "message": "Acara beserta relasinya berhasil dibuat!"}, status=201)
        
        except Exception as e:
            print(f"Error Database: {str(e)}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)