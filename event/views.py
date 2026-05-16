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

    context = {
        'events': events,
        'venues': venues,
        'artists': artists,
    }

    return render(request, "event_list_page.html", context)
    
def get_events(request):
    filter_artist = request.GET.get('artist', '')
    filter_venue = request.GET.get('venue', '')
    search_query = request.GET.get('search', '')

    query_get_event = """
        SELECT e.event_title, TO_CHAR(e.event_datetime, 'YYYY-MM-DD HH24:MI') as event_datetime, e.emoji, 
                v.venue_name, v.city,
                ARRAY_AGG(DISTINCT a.artist_name) AS artists
        FROM EVENT e, VENUE v, ARTIST a, EVENT_ARTIST ea
        WHERE e.venue_id = v.venue_id
                and e.event_id = ea.event_id
                and a.artist_id = ea.artist_id 
        
    """
    params = []

    if search_query:
        query_get_event += " AND (e.event_title ILIKE %s OR a.artist_name ILIKE %s)"
        search_param = f"%{search_query}%"
        params.append(search_param) # judul event
        params.append(search_param) # nama artis

    if filter_artist:
        query_get_event += " AND artist = %s"
        params.append(filter_artist)
    
    if filter_venue:
        query_get_event += " AND venue_name = %s"
        params.append(filter_venue)

    query_get_event += """ GROUP BY event_title, e.event_datetime, v.venue_name, v.city, e.emoji
                            ORDER BY e.event_title ASC; """

    rows = execute_query(query_get_event, tuple(params), fetch=True)
    print(rows)
    
    # for r in rows:
    #     print(r)

    return rows

def get_venues(request): 
    query_get_venues = """
        SELECT venue_name
        FROM VENUE;
    """
    params = []

    rows = execute_query(query_get_venues, tuple(params), fetch=True)
    
    # for r in rows:
    #     print(r)

    return rows

def get_artist(request):
    query_get_artist = """
        SELECT artist_name
        FROM ARTIST;
    """
    params = []

    rows = execute_query(query_get_artist, tuple(params), fetch=True)
    
    # for r in rows:
    #     print(r)

    return rows
