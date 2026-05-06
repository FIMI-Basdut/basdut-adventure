from django.shortcuts import render, redirect

DUMMY_ORDERS = [
    {
        "order_id": "ORD-354F4",
        "order_date": "2026-07-03 10:15",
        "payment_status": "PAID", # Sesuai dengan {% if order.payment_status == "PAID" %}
        "total_amount": 300000,
        "customer_name": "Alice Johnson" # Dibutuhkan untuk avatar dan nama di tabel
    },
    {
        "order_id": "ORD-D3E42",
        "order_date": "2026-07-05 14:20",
        "payment_status": "PENDING",
        "total_amount": 150000,
        "customer_name": "Bob Smith"
    },
    {
        "order_id": "ORD-2504C",
        "order_date": "2026-07-10 09:00",
        "payment_status": "CANCELLED",
        "total_amount": 0,
        "customer_name": "Charlie Brown"
    },
    {
        "order_id": "ORD-DF1AC",
        "order_date": "2026-07-12 16:45",
        "payment_status": "PAID",
        "total_amount": 500000,
        "customer_name": "David Miller"
    },
    {
        "order_id": "ORD-AE6C3",
        "order_date": "2026-07-15 11:30",
        "payment_status": "PENDING",
        "total_amount": 200000,
        "customer_name": "Eve Wilson"
    }
]

def show_order_list(request):
    user_role = "ADMIN" 
    
    total_orders = len(DUMMY_ORDERS)
    total_paid = sum(1 for o in DUMMY_ORDERS if o["payment_status"] == "PAID")
    total_pending = sum(1 for o in DUMMY_ORDERS if o["payment_status"] == "PENDING")
    
    
    revenue_raw = sum(o["total_amount"] for o in DUMMY_ORDERS if o["payment_status"] == "PAID")
    total_revenue = f"{revenue_raw:,}".replace(",", ".")

    context = {
        "orders": DUMMY_ORDERS,
        "user_role": user_role, 
        "total_orders": total_orders,
        "total_paid": total_paid,
        "total_pending": total_pending,
        "total_revenue": f"Rp {total_revenue}",
    }
    
    return render(request, 'list-order.html', context)

def show_order_create(request):
    return render(request, 'create-order.html')

def dummy_order_action(request):
    return redirect('order:show_order_list')