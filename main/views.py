from django.shortcuts import render, redirect




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