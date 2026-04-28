from django.shortcuts import render, redirect

# --- DATA HARDCODE SEAT ---
DUMMY_SEATS = [
    {"id": 1, "section": "WVIP", "row": "A", "number": "1", "venue": "Jakarta Convention Center", "status": "TERISI"},
    {"id": 2, "section": "WVIP", "row": "A", "number": "2", "venue": "ICE BSD city", "status": "TERSEDIA"},
    {"id": 3, "section": "FESTIVAL", "row": "C", "number": "6", "venue": "Jakarta Convention Center", "status": "TERSEDIA"},
    {"id": 4, "section": "CAT 1", "row": "B", "number": "10", "venue": "Jakarta Convention Center", "status": "TERSEDIA"},
    {"id": 5, "section": "WVIP", "row": "A", "number": "3", "venue": "ICE BSD city", "status": "TERISI"},
    {"id": 6, "section": "WVIP", "row": "A", "number": "4", "venue": "Jakarta Convention Center", "status": "TERSEDIA"},
    {"id": 7, "section": "FESTIVAL", "row": "C", "number": "10", "venue": "ICE BSD city", "status": "TERSEDIA"},
    {"id": 8, "section": "CAT 1", "row": "B", "number": "11", "venue": "Jakarta Convention Center", "status": "TERSEDIA"},
]

DUMMY_TICKETS = [
    {
        "id": 1, "code": "TTK-EVT001-VIP-001", "event": "Konser Melodi Senja", 
        "status": "VALID", "category": "VIP", "date": "2026-05-15 19:00", 
        "price": "Rp 750.000", "venue": "Jakarta Convention Center", 
        "order": "ord_001", "seat": "VIP B-1", "customer": "Budi Santoso"
    },
    {
        "id": 2, "code": "TTK-EVT001-REG-002", "event": "Konser Melodi Senja", 
        "status": "TERPAKAI", "category": "REGULER", "date": "2026-05-15 19:00", 
        "price": "Rp 350.000", "venue": "Jakarta Convention Center", 
        "order": "ord_002", "seat": "FESTIVAL", "customer": "Siti Aminah"
    },
     {
        "id": 3, "code": "TTK-EVT001-VIP-001", "event": "Konser Melodi Senja", 
        "status": "TERPAKAI", "category": "VIP", "date": "2026-05-15 19:00", 
        "price": "Rp 750.000", "venue": "Jakarta Convention Center", 
        "order": "ord_003", "seat": "VIP B-1", "customer": "Dita Karyadi"
    },
    {
        "id": 4, "code": "TTK-EVT001-REG-002", "event": "Konser Melodi Senja", 
        "status": "TERPAKAI", "category": "REGULER", "date": "2026-05-15 19:00", 
        "price": "Rp 350.000", "venue": "Jakarta Convention Center", 
        "order": "ord_004", "seat": "FESTIVAL", "customer": "Bobon Rintarto"
    }
]

def show_seat(request):
    total_kursi = len(DUMMY_SEATS)
    tersedia = sum(1 for s in DUMMY_SEATS if s["status"] == "TERSEDIA")
    terisi = sum(1 for s in DUMMY_SEATS if s["status"] == "TERISI")

    context = {
        "seats": DUMMY_SEATS,
        "total_kursi": total_kursi,
        "tersedia": tersedia,
        "terisi": terisi,
    }
    return render(request, 'seat.html', context)

def dummy_seat_action(request):
    return redirect('main:show_seat')


def show_mantap(request):
    return render(request, "mantap.html")

def show_ticket(request):
    total_tickets = len(DUMMY_TICKETS)
    valid_tickets = sum(1 for t in DUMMY_TICKETS if t["status"] == "VALID")
    used_tickets = sum(1 for t in DUMMY_TICKETS if t["status"] == "TERPAKAI")

    context = {
        "tickets": DUMMY_TICKETS,
        "total_tickets": total_tickets,
        "valid_tickets": valid_tickets,
        "used_tickets": used_tickets,
    }
    return render(request, 'ticket.html', context)

def dummy_ticket_action(request):
    return redirect('main:show_ticket')