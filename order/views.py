from django.shortcuts import render, redirect
from django.contrib import messages
from basdut_adventure.db import get_connection


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

def show_order_create(request):
    return render(request, 'create-order.html')

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