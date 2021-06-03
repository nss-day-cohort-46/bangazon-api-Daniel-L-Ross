from django.urls import path
from .views import favorited_seller_list
from .views import expensive_product_list

urlpatterns = [
    path('reports/favoritedsellers', favorited_seller_list),
    path('reports/expensiveproducts', expensive_product_list)
]
