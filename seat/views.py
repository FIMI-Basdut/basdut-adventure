from django.shortcuts import render,redirect

DUMMY_SEATS = [
    {"id": 1, "section": "WVIP", "row": "A", "number": "1", "venue": "Jakarta Convention Center", "status": "TERISI"},
    {"id": 2, "section": "WVIP", "row": "A", "number": "2", "venue": "Jakarta Convention Center", "status": "TERSEDIA"},
    {"id": 3, "section": "VIP", "row": "B", "number": "15", "venue": "Jakarta Convention Center", "status": "TERISI"},
    {"id": 4, "section": "Category 1", "row": "C", "number": "22", "venue": "Jakarta Convention Center", "status": "TERSEDIA"},
    {"id": 5, "section": "General Admission", "row": "-", "number": "-", "venue": "Taman Impian Jayakarta", "status": "TERSEDIA"},
    {"id": 6, "section": "General Admission", "row": "-", "number": "-", "venue": "Taman Impian Jayakarta", "status": "TERISI"},
    {"id": 7, "section": "VVIP", "row": "A", "number": "5", "venue": "Bandung Hall Center", "status": "TERISI"},
    {"id": 8, "section": "Regular", "row": "D", "number": "10", "venue": "Bandung Hall Center", "status": "TERSEDIA"},
    {"id": 9, "section": "WVIP", "row": "A", "number": "1", "venue": "ICE BSD City", "status": "TERISI"},
    {"id": 10, "section": "Category 2", "row": "E", "number": "34", "venue": "ICE BSD City", "status": "TERSEDIA"},
    {"id": 11, "section": "Category 2", "row": "E", "number": "35", "venue": "ICE BSD City", "status": "TERSEDIA"},
    {"id": 12, "section": "VIP", "row": "B", "number": "1", "venue": "ICE BSD City", "status": "TERISI"},
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
