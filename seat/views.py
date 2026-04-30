from django.shortcuts import render,redirect

DUMMY_SEATS = [
    {"id": 1, "section": "WVIP", "row": "A", "number": "1", "venue": "Jakarta Convention Center", "status": "TERISI"},
    {"id": 2, "section": "WVIP", "row": "A", "number": "2", "venue": "ICE BSD city", "status": "TERSEDIA"},
    {"id": 3, "section": "FESTIVAL", "row": "-", "number": "-", "venue": "Jakarta Convention Center", "status": "TERSEDIA"},
    {"id": 4, "section": "CAT 1", "row": "B", "number": "10", "venue": "Jakarta Convention Center", "status": "TERSEDIA"},
    {"id": 1, "section": "WVIP", "row": "A", "number": "1", "venue": "ICE BSD city", "status": "TERISI"},
    {"id": 2, "section": "WVIP", "row": "A", "number": "2", "venue": "Jakarta Convention Center", "status": "TERSEDIA"},
    {"id": 3, "section": "FESTIVAL", "row": "-", "number": "-", "venue": "ICE BSD city", "status": "TERSEDIA"},
    {"id": 4, "section": "CAT 1", "row": "B", "number": "10", "venue": "Jakarta Convention Center", "status": "TERSEDIA"},
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
    return redirect('seat:show_seat')
