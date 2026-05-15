from django.shortcuts import render, redirect
from django.contrib import messages
from basdut_adventure.db import get_connection
import uuid

def show_promotions(request):
    user_role = request.session.get('role')
    discount_type = request.GET.get("discount_type") # list promotion based on discount type
    search_code = request.GET.get("input_kode_promo")
    
    # Getting all the promo data needed
    
    conn = get_connection()
    
    try:
        with conn.cursor() as cur:
                query = """
                        SELECT
                            p.promotion_id,
                            p.promo_code,
                            p.discount_type,
                            p.discount_value,
                            p.start_date,
                            p.end_date,
                            p.usage_limit,
                            COUNT(op.promotion_id) AS total_usage
                        FROM promotion p
                        LEFT JOIN order_promotion op
                            ON p.promotion_id = op.promotion_id
                        """

                params = []

                if discount_type:
                    query += " WHERE p.discount_type = %s"
                    params.append(discount_type)
                
                # if search_code:
                #     query += " AND p.promo_code LIKE %s"
                #     params.append(f"%{search_code}%")

                query += """
                    GROUP BY
                        p.promotion_id,
                        p.promo_code,
                        p.discount_type,
                        p.discount_value,
                        p.start_date,
                        p.end_date,
                        p.usage_limit
                """

                cur.execute(query, params)
                rows = cur.fetchall()
                
                promos = []

                for row in rows:
                    promo = {
                        'id': row[0],          # promotion_id
                        'code': row[1],        # promo_code
                        'type': row[2],        # discount_type
                        'value': row[3],       # discount_value
                        'sdate': row[4],       # start_date
                        'edate': row[5],       # end_date
                        'max': row[6],         # usage_limit
                        'used': row[7]         # total_usage
                    }
                    promos.append(promo)
        conn.commit()
        
    except Exception:
        # If any query fails, undo everything
        messages.error(request, 'Uh oh! Something is wrong.')
        conn.rollback()
        raise
    
    finally:
        conn.close()
    
    total_promos = len(promos)
    total_usage = sum(promo["used"] for promo in promos)
    percentage_types = sum(1 for promo in promos if promo["type"] == "PERCENTAGE")

    context = {
        "promos": promos,
        "user_role": user_role,
        "total_promos": total_promos,
        "total_usage": f"{total_usage}x",
        "percentage_types": percentage_types,
    }
    
    return render(request, 'list-promotion.html', context)

def dummy_promo_action(request):
    return redirect('promotion:show_promotions')

def create_promotion(request):
    if request.method == "POST" and request.session.get('role') == 'Admin':
        kode_promo = request.POST.get("promo_code")
        tipe_promo = request.POST.get("promo_type")
        nominal_diskon = request.POST.get("discount_value")
        tanggal_awal = request.POST.get("start_date")
        tanggal_akhir = request.POST.get("end_date")
        batas_penggunaan = request.POST.get("max_usage")
        promo_id = str(uuid.uuid4())
        
        conn = get_connection()
        
        try:
            with conn.cursor() as cur:
                  cur.execute(
                    """
                    INSERT INTO promotion 
                    (promotion_id, 
                    promo_code, 
                    discount_type, 
                    discount_value, 
                    start_date, 
                    end_date, 
                    usage_limit)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    [promo_id, kode_promo, tipe_promo, nominal_diskon, tanggal_awal, tanggal_akhir, batas_penggunaan]
                  )

            conn.commit()
            messages.success(request, 'The promotion has been created.')
            return redirect('promotion:show_promotions')
            
        except Exception as e:
            # If any query fails, undo everything
            conn.rollback()
            messages.error(request, 'Uh oh! Something is wrong.')
            raise
        
        finally:
            conn.close()
            
    
    messages.error(request, 'Uh oh! Something is wrong.')
    return redirect('promotion:show_promotions')
        
def delete_promotion(request):
    if request.method == "POST" and request.session.get('role') == 'Admin':
        promo_id = request.POST.get("promotion_id")
        
        conn = get_connection()
        
        try:
            with conn.cursor() as cur:
                  cur.execute(
                    """
                    DELETE FROM promotion WHERE promotion_id = %s
                    """,
                    [promo_id]
                  )

            conn.commit()
            messages.success(request, 'The promotion has been deleted.')
            return redirect('promotion:show_promotions')
            
        except Exception as e:
            # If any query fails, undo everything
            conn.rollback()
            messages.error(request, 'Uh oh! Something is wrong.')
            raise
        
        finally:
            conn.close()
    
    messages.error(request, 'Uh oh! Something is wrong.')
    return redirect('promotion:show_promotions')
        
def update_promotion(request):
    if request.method == "POST" and request.session.get('role') == 'Admin':
        kode_promo = request.POST.get("promo_code")
        tipe_promo = request.POST.get("promo_type")
        nominal_diskon = request.POST.get("discount_value")
        tanggal_awal = request.POST.get("start_date")
        tanggal_akhir = request.POST.get("end_date")
        batas_penggunaan = request.POST.get("max_usage")
        promo_id = request.POST.get("promo_id")
        
        conn = get_connection()
        
        try:
            with conn.cursor() as cur:
                  cur.execute(
                    """
                    UPDATE promotion 
                    SET
                        promo_code = %s, 
                        discount_type = %s, 
                        discount_value = %s, 
                        start_date = %s, 
                        end_date = %s, 
                        usage_limit = %s
                    WHERE promotion_id = %s
                    
                    """,
                    [kode_promo, tipe_promo, nominal_diskon, tanggal_awal, tanggal_akhir, batas_penggunaan, promo_id]
                  )

            conn.commit()
            messages.success(request, 'The promotion has been updated.')
            return redirect('promotion:show_promotions')
            
        except Exception as e:
            # If any query fails, undo everything
            conn.rollback()
            messages.error(request, 'Uh oh! Something is wrong.')
            raise
        
        finally:
            conn.close()
            
    
    messages.error(request, 'Uh oh! Something is wrong.')
    return redirect('promotion:show_promotions')