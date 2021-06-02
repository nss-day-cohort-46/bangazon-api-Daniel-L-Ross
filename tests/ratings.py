from bangazonapi.models.productrating import ProductRating
import json
import datetime
from rest_framework import status
from rest_framework.test import APITestCase


class RatingsTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account, sample category, and sample product
        """
        url = "/register"
        data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
                "address": "100 Infinity Way", "phone_number": "555-1212", "first_name": "Steve", "last_name": "Brownlee"}
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # create a second user for averaging ratings
        data = {"username": "smeve", "password": "Admin10*", "email": "smeve@stevebrownlee.com",
                "address": "100 Infinity Way", "phone_number": "555-1212", "first_name": "Smeve", "last_name": "Brownlee"}
        response = self.client.post(url, data, format='json')
        
        url = "/productcategories"
        data = {"name": "Sporting Goods"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "Sporting Goods")

        url = "/products"
        data = {
            "name": "Kite",
            "price": 14.99,
            "quantity": 60,
            "description": "It flies high",
            "category_id": 1,
            "location": "Pittsburgh"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "Kite")
        self.assertEqual(json_response["price"], 14.99)
        self.assertEqual(json_response["quantity"], 60)
        self.assertEqual(json_response["description"], "It flies high")
        self.assertEqual(json_response["location"], "Pittsburgh")

    def test_create_rating(self):
        """
        Ensure we can create a new rating,
        THEN ensure the avg_rating key exists AND is correct.
        """
        url = "/products/1/rate"
        data = {
            "rating": 5
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # add another rating, then check the average
        product_rating = ProductRating()
        product_rating.product_id = 1
        product_rating.customer_id = 2
        product_rating.rating = 0
        product_rating.save()
        url="/products/1"
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(json_response["average_rating"], 2.5)