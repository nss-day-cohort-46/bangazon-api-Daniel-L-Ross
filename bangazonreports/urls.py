from django.urls import path
from .views import favorited_seller_list

urlpatterns = [
    path('reports/favoritedsellers', favorited_seller_list)
]
