from django.shortcuts import render, redirect

# Data Dummy Promosi
DUMMY_PROMOS = [
    {
        "id": "1d5afa98-bc36-42dd-b562-c10207e7d9cb",
        "code": "FESTIVE10",
        "type": "PERCENTAGE",
        "value": "10%",  # Diformat string agar langsung siap tampil di HTML
        "start_date": "2026-07-01",
        "end_date": "2026-07-31",
        "usage_count": 0, # Tambahan dummy untuk melengkapi tabel HTML
        "max_usage": 100,
        "icon_color": "purple" # Tambahan untuk style UI
    },
    {
        "id": "0467f315-a328-4295-a317-7df5d669e234",
        "code": "EARLY50",
        "type": "NOMINAL",
        "value": "Rp 50,000",
        "start_date": "2026-07-05",
        "end_date": "2026-07-20",
        "usage_count": 12,
        "max_usage": 50,
        "icon_color": "orange"
    },
    {
        "id": "ab5412af-73bb-467c-be3b-167cbb6718cb",
        "code": "VIP20",
        "type": "PERCENTAGE",
        "value": "20%",
        "start_date": "2026-07-10",
        "end_date": "2026-08-10",
        "usage_count": 28,
        "max_usage": 30,
        "icon_color": "purple"
    },
    {
        "id": "ce3400b9-39c4-4496-bdc6-27c622c218d1",
        "code": "SAVE25K",
        "type": "NOMINAL",
        "value": "Rp 25,000",
        "start_date": "2026-08-01",
        "end_date": "2026-08-31",
        "usage_count": 45,
        "max_usage": 80,
        "icon_color": "orange"
    },
    {
        "id": "3d5d748b-3b39-4ef9-b6bd-90f5d35d2f9f",
        "code": "FLASH15",
        "type": "PERCENTAGE",
        "value": "15%",
        "start_date": "2026-07-15",
        "end_date": "2026-07-18",
        "usage_count": 40,
        "max_usage": 40,
        "icon_color": "purple"
    },
    {
        "id": "156c26de-b259-4924-9118-264fdde9efc3",
        "code": "MEGA100K",
        "type": "NOMINAL",
        "value": "Rp 100,000",
        "start_date": "2026-08-05",
        "end_date": "2026-09-05",
        "usage_count": 5,
        "max_usage": 20,
        "icon_color": "orange"
    }
]

def show_promotions(request):
    user_role = "ADMIN" 
    
    total_promos = len(DUMMY_PROMOS)
    total_usage = sum(promo["usage_count"] for promo in DUMMY_PROMOS)
    percentage_types = sum(1 for promo in DUMMY_PROMOS if promo["type"] == "PERCENTAGE")

    context = {
        "promos": DUMMY_PROMOS,
        "user_role": user_role,
        "total_promos": total_promos,
        "total_usage": f"{total_usage}x",
        "percentage_types": percentage_types,
    }
    
    return render(request, 'list-promotion.html', context)

def dummy_promo_action(request):
    return redirect('promotion:show_promotions')