"""Module for generating favorited sellers by customer report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection

def favorited_seller_list(request):
    """Function to build an HTML report of a user's favorited sellers"""
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    c.id as customer_id,
                    a.first_name || ' ' || a.last_name as customer_name,
                    b.first_name || ' ' || b.last_name as seller_name
                FROM bangazonapi_favorite f
                JOIN bangazonapi_customer c ON c.id = f.customer_id
                JOIN auth_user a ON c.user_id = a.id
                JOIN bangazonapi_customer d ON d.id = f.seller_id
                JOIN auth_user b ON d.user_id = b.id
            """)

            dataset = db_cursor.fetchall()

            favorited_seller_by_user = {}

            for row in dataset:
                customer_id = row["customer_id"]

                if customer_id in favorited_seller_by_user:
                    favorited_seller_by_user[customer_id]['sellers'].append(row["seller_name"])

                else:
                    favorited_seller_by_user[customer_id] = {}
                    favorited_seller_by_user[customer_id]["customer_name"] = row["customer_name"]
                    favorited_seller_by_user[customer_id]['sellers'] = [row["seller_name"]]

        list_of_user_with_favorited_sellers = favorited_seller_by_user.values()

        template = 'customers/list_with_favorited_sellers.html'
        context = {
            'favorited_sellers_list': list_of_user_with_favorited_sellers
        }

        return render(request, template, context)