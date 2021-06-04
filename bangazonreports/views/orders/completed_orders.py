"""Module for generating completed orders report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection

def completed_order_list(request):
    """Function to build an HTML report of completed orders"""
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT 
                    b_o.id as order_id,
                    a.first_name ||' '|| a.last_name as customer_name,
                    pay.id as payment_type_id,
                    pay.merchant_name as payment_card_type,
                    SUM(p.price) as order_total
                FROM bangazonapi_order b_o
                INNER JOIN bangazonapi_customer c ON c.id = b_o.customer_id
                INNER JOIN auth_user a ON a.id = c.user_id
                INNER JOIN bangazonapi_payment pay ON pay.id = b_o.payment_type_id 
                LEFT JOIN bangazonapi_orderproduct op ON op.order_id = b_o.id
                LEFT JOIN bangazonapi_product p ON p.id = op.product_id
                WHERE b_o.payment_type_id IS NOT NULL
                GROUP BY b_o.id
            """)

            dataset = db_cursor.fetchall()

            completed_orders = dataset

        template = 'orders/list_with_completed_orders.html'
        context = {
            'completed_orders': completed_orders
        }

        return render(request, template, context)