"""Module for generating report of expensive products"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection

def expensive_product_list(request):
    """Function to build an HTML report of products over $1000"""
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    p.id as product_id,
                    p.name,
                    p.description,
                    p.price
                FROM bangazonapi_product p
                WHERE p.price >= 1000
            """)

            dataset = db_cursor.fetchall()

            expensive_products = dataset

        template = 'products/list_expensive_products.html'
        context = {
            'expensive_products_list': expensive_products
        }

        return render(request, template, context)