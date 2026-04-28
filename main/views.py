from django.shortcuts import render

# Create your views here.
def show_mantap(request):
    return render(request, "mantap.html")

def show_ticket(request):
    return render(request, 'ticket.html')

def show_seat(request):
    return render(request, 'seat.html')