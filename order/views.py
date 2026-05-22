from django.shortcuts import render, redirect
from django.contrib import messages
from basdut_adventure.db import get_connection
import uuid, psycopg2

def show_order_list(request):
    user_role = request.session.get('role')
    
    conn = get_connection()
    
    if user_role == 'Admin':
    
        try:
            with conn.cursor() as cur:

                    cur.execute(
                        """
                        SELECT * FROM ticket_order
                        """, 
                    )
                    rows = cur.fetchall()
                    
                    orders = []

                    for row in rows:
                        # get customer full name
                        cur.execute(
                            """
                            SELECT full_name
                            FROM Customer
                            WHERE customer_id = %s
                            """,
                            [row[4]]
                        )
                        
                        second_row = cur.fetchone()
                        
                        if second_row is None:
                            raise ValueError("Customer name not found")
                        
                        order = {
                            'id': row[0],               # order_id
                            'date': row[1],             # order_date
                            'status': row[2],           # payment_status
                            'amount': row[3],           # total_amount
                            'cust_id': row[4],          # customer_id
                            'cust_name': second_row[0]  # customer_name
                        }
                        orders.append(order)
            conn.commit()
            
        except Exception:
            # If any query fails, undo everything
            messages.error(request, 'Uh oh! Something is wrong.')
            conn.rollback()
            raise
        
        finally:
            conn.close()
            
    elif user_role == 'Organizer':
    
        try:
            with conn.cursor() as cur:

                    cur.execute(
                        """
                        SELECT TO.order_id, TO.order_date, TO.payment_status, TO.total_amount, TO.customer_id
                        FROM ticket_order as TO
                        JOIN ticket as T ON T.torder_id = TO.order_id
                        JOIN ticket_category as TC ON T.tcategory_id = TC.category_id
                        JOIN event as E ON TC.tevent_id = E.event_id
                        WHERE E.organization_id = %s
                        """, [request.session.get('user_id')]
                    )
                    rows = cur.fetchall()
                    
                    orders = []

                    for row in rows:
                        # get customer full name
                        cur.execute(
                            """
                            SELECT full_name
                            FROM Customer
                            WHERE customer_id = %s
                            """,
                            [row[4]]
                        )
                        
                        second_row = cur.fetchone()
                        
                        if second_row is None:
                            raise ValueError("Customer name not found")
                        
                        order = {
                            'id': row[0],               # order_id
                            'date': row[1],             # order_date
                            'status': row[2],           # payment_status
                            'amount': row[3],           # total_amount
                            'cust_id': row[4],          # customer_id
                            'cust_name': second_row[0]  # customer_name
                        }
                        orders.append(order)
            conn.commit()
            
        except Exception:
            # If any query fails, undo everything
            messages.error(request, 'Uh oh! Something is wrong.')
            conn.rollback()
            raise
        
        finally:
            conn.close()
    
    elif user_role == 'Customer':
    
        try:
            with conn.cursor() as cur:

                    cur.execute(
                        """
                        SELECT * FROM ticket_order as TI
                        JOIN customer as C ON TI.customer_id = C.customer_id
                        WHERE C.user_id = %s
                        """, [request.session.get('user_id')]
                    )
                    rows = cur.fetchall()
                    
                    orders = []

                    for row in rows:
                        
                        order = {
                            'id': row[0],               # order_id
                            'date': row[1],             # order_date
                            'status': row[2],           # payment_status
                            'amount': row[3],           # total_amount
                            'cust_id': row[4],          # customer_id
                        }
                        orders.append(order)
            conn.commit()
            
        except Exception:
            # If any query fails, undo everything
            messages.error(request, 'Uh oh! Something is wrong.')
            conn.rollback()
            raise
        
        finally:
            conn.close()
    
    total_orders = len(orders)
    total_paid = sum(1 for o in orders if o["status"] == "Lunas")
    total_pending = sum(1 for o in orders if o["status"] == "Pending")
    revenue_raw = sum(o["amount"] for o in orders if o["status"] == "Lunas")
    
    context = {
        "orders": orders,
        "user_role": user_role, 
        "total_orders": total_orders,
        "total_paid": total_paid,
        "total_pending": total_pending,
        "total_revenue": f"Rp {revenue_raw}",
    }
    
    return render(request, 'list-order.html', context)

def show_order_create(request, event_id):
    user_role = request.session.get('role')
    user_id = request.session.get('user_id')
    
    conn = get_connection()
    
    try:
        # --- GET EVENT DETAILS, CATEGORIES, AND SEATS FOR DISPLAY ---
        if request.method == "GET":
            with conn.cursor() as cur:
                # 1. Fetch Event Details (Added venue_id to the SELECT)
                cur.execute(
                    """
                    SELECT event_id, event_title, event_datetime, venue_id 
                    FROM EVENT 
                    WHERE event_id = %s
                    """,
                    [event_id]
                )
                event_row = cur.fetchone()
                
                if not event_row:
                    messages.error(request, "Event not found.")
                    return redirect('order:show_order_list')
                    
                event_context = {
                    'id': event_row[0],
                    'title': event_row[1],
                    'datetime': event_row[2].strftime('%Y-%m-%d %H:%M') if event_row[2] else 'TBD',
                    'venue_id': event_row[3]
                }

                # 2. Fetch Ticket Categories 
                cur.execute(
                    """
                    SELECT category_id, category_name, quota, price 
                    FROM TICKET_CATEGORY 
                    WHERE tevent_id = %s
                    """,
                    [event_id]
                )
                category_rows = cur.fetchall()
                categories_context = [{'id': r[0], 'name': r[1], 'quota': r[2], 'price': r[3]} for r in category_rows]

                # 3. Fetch Seats for this Venue
                cur.execute(
                    """
                    SELECT seat_id, section, row_number, seat_number 
                    FROM SEAT 
                    WHERE venue_id = %s
                    ORDER BY section, row_number, seat_number
                    """,
                    [event_context['venue_id']]
                )
                seat_rows = cur.fetchall()
                
                seats_context = []
                for row in seat_rows:
                    seats_context.append({
                        'id': row[0],
                        'section': row[1],
                        'row_number': row[2],
                        'seat_number': row[3]
                    })

            # Pass everything to the template
            return render(request, 'create-order.html', {
                'event': event_context,
                'categories': categories_context,
                'seats': seats_context
            })

        # --- HANDLE FORM SUBMISSION (POST) ---
        
        elif request.method == "POST":
            if user_role != 'Customer':
                messages.error(request, 'Only customers can create orders.')
                return redirect('order:show_order_list')
                
            # Grab form inputs
            promo_code_input = request.POST.get("promo_code", "").strip().upper()
            category_id = request.POST.get("category_id")
            quantity = int(request.POST.get("quantity", 1))
            seat_id = request.POST.get("seat_id", "").strip() or None

            # Convert total_amount to float so we can do math on it
            try:
                total_amount = float(request.POST.get("total_amount", 0))
            except ValueError:
                total_amount = 0.0
            
            order_id = str(uuid.uuid4())
            promotion_id = None
            
            with conn.cursor() as cur:
                # 1. Fetch customer_id
                cur.execute("SELECT customer_id FROM customer WHERE user_id = %s", [user_id])
                customer_row = cur.fetchone()
                if not customer_row:
                    raise ValueError("Customer profile not found")
                customer_id = customer_row[0]
                
                # 2. Evaluate promo code and calculate discounted total
                if promo_code_input:
                    cur.execute(
                        """
                        SELECT promotion_id, discount_type, discount_value 
                        FROM promotion 
                        WHERE UPPER(promo_code) = %s
                        """, 
                        [promo_code_input]
                    )
                    promo_row = cur.fetchone()
                    
                    if promo_row:
                        promotion_id = promo_row[0]
                        discount_type = promo_row[1]
                        discount_value = float(promo_row[2])
                        
                        if discount_type == 'PERCENTAGE':
                            total_amount -= total_amount * (discount_value / 100.0)
                        elif discount_type == 'NOMINAL':
                            total_amount -= discount_value
                            
                        if total_amount < 0:
                            total_amount = 0
                    else:
                        raise ValueError(f'ERROR: Kode promo "{promo_code_input}" tidak terdaftar.')

                # 3. Insert the main ORDER record
                cur.execute(
                    """
                    INSERT INTO TICKET_ORDER (order_id, order_date, payment_status, total_amount, customer_id)
                    VALUES (%s, CURRENT_TIMESTAMP, %s, %s, %s)
                    """,
                    [order_id, 'Pending', total_amount, customer_id]
                )

                # 4. Insert TICKET(s) — MUST happen BEFORE order_promotion insert
                #    because VALIDATE_PROMOTION_DATE trigger joins TICKET to get event_date.
                for _ in range(quantity):
                    ticket_id = str(uuid.uuid4())
                    ticket_code = f"TKT-{ticket_id[:8].upper()}"
                    cur.execute(
                        """
                        INSERT INTO TICKET (ticket_id, ticket_code, tcategory_id, torder_id)
                        VALUES (%s, %s, %s, %s)
                        """,
                        [ticket_id, ticket_code, category_id, order_id]
                    )
                    # Assign seat if provided (only relevant for first ticket / single seat)
                    if seat_id and _ == 0:
                        cur.execute(
                            """
                            INSERT INTO HAS_RELATIONSHIP (seat_id, ticket_id)
                            VALUES (%s, %s)
                            """,
                            [seat_id, ticket_id]
                        )

                # 5. Insert order_promotion AFTER tickets exist — triggers can now resolve event_date
                if promotion_id:
                    order_promotion_id = str(uuid.uuid4())
                    cur.execute(
                        """
                        INSERT INTO order_promotion (order_promotion_id, order_id, promotion_id)
                        VALUES (%s, %s, %s)
                        """,
                        [order_promotion_id, order_id, promotion_id]
                    )
                
            conn.commit()
            messages.success(request, 'Pesanan Anda berhasil dibuat!')
            return redirect('order:show_order_list')
            
    # 2. CATCH THE TRIGGER ERRORS HERE
    except psycopg2.DatabaseError as e:
        conn.rollback()  # Undo the TICKET_ORDER insert if the promo trigger fails!
        
        custom_trigger_message = e.diag.message_primary
        if custom_trigger_message:
            messages.error(request, custom_trigger_message)
        else:
            messages.error(request, f"Database Error: {str(e)}")
            
        return redirect('order:show_order_create', event_id=event_id)
        
    # 3. CATCH OTHER PYTHON ERRORS
    except Exception as e:
        conn.rollback()
        messages.error(request, str(e) if "ERROR:" in str(e) else 'Uh oh! Something went wrong.')
        return redirect('order:show_order_create', event_id=event_id)
        
    finally:
        conn.close()

def dummy_order_action(request):
    return redirect('order:show_order_list')

def delete_order(request):
    if request.method == "POST" and request.session.get('role') == 'Admin':
        order_id = request.POST.get("order_id")
        
        conn = get_connection()
        
        try:
            with conn.cursor() as cur:
                  cur.execute(
                    """
                    DELETE FROM ticket_order WHERE order_id = %s
                    """,
                    [order_id]
                  )

            conn.commit()
            messages.success(request, 'The order has been deleted.')
            return redirect('order:show_order_list')
            
        except Exception as e:
            # If any query fails, undo everything
            conn.rollback()
            messages.error(request, 'Uh oh! Something is wrong.')
            raise
        
        finally:
            conn.close()
    
    messages.error(request, 'Uh oh! Something is wrong.')
    return redirect('order:show_order_list')
        
def update_order(request):
    if request.method == "POST" and request.session.get('role') == 'Admin':
        order_id = request.POST.get("order_id")
        status_order = request.POST.get("status")
        
        conn = get_connection()
        
        try:
            with conn.cursor() as cur:
                  cur.execute(
                    """
                    UPDATE ticket_order
                    SET
                        payment_status = %s
                    WHERE order_id = %s
                    
                    """,
                    [status_order, order_id]
                  )

            conn.commit()
            messages.success(request, 'The order has been updated.')
            return redirect('order:show_order_list')
            
        except Exception as e:
            # If any query fails, undo everything
            conn.rollback()
            messages.error(request, 'Uh oh! Something is wrong.')
            raise
        
        finally:
            conn.close()
            
    
    messages.error(request, 'Uh oh! Something is wrong.')
    return redirect('order:show_order_list')