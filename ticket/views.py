from django.shortcuts import render, redirect

DUMMY_TICKETS = [
    {
        "id": 1, "code": "TTK-EVT001-WVIP-001", "event": "Konser Melodi Senja", 
        "status": "VALID", "category": "WVIP", "date": "2026-05-15 19:00", 
        "price": "Rp 1.500.000", "venue": "Jakarta Convention Center", 
        "order": "ord_001", "seat": "WVIP A-1", "customer": "Budi Santoso"
    },
    {
        "id": 2, "code": "TTK-EVT001-VIP-045", "event": "Konser Melodi Senja", 
        "status": "TERPAKAI", "category": "VIP", "date": "2026-05-15 19:00", 
        "price": "Rp 750.000", "venue": "Jakarta Convention Center", 
        "order": "ord_002", "seat": "VIP B-15", "customer": "Siti Aminah"
    },
    {
        "id": 3, "code": "TTK-EVT002-GEN-102", "event": "Festival Seni Budaya", 
        "status": "VALID", "category": "General Admission", "date": "2026-05-22 10:00", 
        "price": "Rp 150.000", "venue": "Taman Impian Jayakarta", 
        "order": "ord_005", "seat": "FESTIVAL", "customer": "Izzudin Abdul Rasyid"
    },
    {
        "id": 4, "code": "TTK-EVT002-GEN-103", "event": "Festival Seni Budaya", 
        "status": "TERPAKAI", "category": "General Admission", "date": "2026-05-22 10:00", 
        "price": "Rp 150.000", "venue": "Taman Impian Jayakarta", 
        "order": "ord_005", "seat": "FESTIVAL", "customer": "Izzudin Abdul Rasyid"
    },
    {
        "id": 5, "code": "TTK-EVT003-VVIP-005", "event": "Malam Akustik Bandung", 
        "status": "VALID", "category": "VVIP", "date": "2026-06-10 18:00", 
        "price": "Rp 2.000.000", "venue": "Bandung Hall Center", 
        "order": "ord_008", "seat": "VVIP A-5", "customer": "Dita Karyadi"
    },
    {
        "id": 6, "code": "TTK-EVT001-CAT1-022", "event": "Konser Melodi Senja", 
        "status": "DIBATALKAN", "category": "Category 1", "date": "2026-05-15 19:00", 
        "price": "Rp 450.000", "venue": "Jakarta Convention Center", 
        "order": "ord_010", "seat": "Category 1 C-22", "customer": "Bobon Rintarto"
    },
    {
        "id": 7, "code": "TTK-EVT004-WVIP-001", "event": "Rock Legends Tour", 
        "status": "VALID", "category": "WVIP", "date": "2026-08-15 20:00", 
        "price": "Rp 2.500.000", "venue": "ICE BSD City", 
        "order": "ord_012", "seat": "WVIP A-1", "customer": "Rina Gunawan"
    }
]

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
    return redirect('ticket:show_ticket')