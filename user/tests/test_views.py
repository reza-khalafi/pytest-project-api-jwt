from django.test import TestCase
import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, RequestsClient
from mixer.backend.django import mixer

from user.authenticate import Authenticate
from user.models import User
from user.modules import hash_password

pytestmark = pytest.mark.django_db


class TestUserAPIViews(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_list(self):
        # Add two user to test db temporary
        user1 = mixer.blend(User, first_name="Mohammad")
        user2 = mixer.blend(User, first_name="Parastoo")

        # Get api url
        url = reverse("get-users")
        # call the url
        response = self.client.get(url)
        print(f"size: {len(response.json())}")
        assert response.json() is not None
        assert len(response.json()) == 2
        assert response.status_code == 200

    def test_user_detail(self):
        # Add two user to test db temporary
        user1 = mixer.blend(User, first_name="Jax")
        user2 = mixer.blend(User, first_name="Mary")

        # Get api url
        url1 = reverse("get-user-detail", kwargs={'pk': 1})
        url2 = reverse("get-user-detail", kwargs={'pk': 3})

        # call the url
        response1 = self.client.get(url1)
        response2 = self.client.get(url2)

        assert response1.json() is not None
        assert response1.status_code == 200
        assert response1.json()["first_name"] == "Jax"

        assert response2.json() is not None
        assert response2.status_code == 400

    def test_create_user(self):
        # Data
        input_data_0 = {

        }

        input_data_1 = {
            "first_name": "Ahmad",
            "last_name": "Jalali",
            "username": "ahmad44",
            "password": "123456"
        }

        input_data_2 = {
            "first_name": "Ahmad Reza",
            "last_name": "Kamali",
            "username": "ahmad44",
            "password": "123456"
        }

        # Get api url
        url = reverse("create-users")

        # call the url
        response0 = self.client.post(url, data=input_data_0)
        response1 = self.client.post(url, data=input_data_1)
        response2 = self.client.post(url, data=input_data_2)

        assert response0.json() is not None
        assert response0.status_code == 400

        assert response1.json() is not None
        assert response1.status_code == 200

        assert response2.json() is not None
        assert response2.status_code == 400
        assert User.objects.count() == 1

    def test_delete_user(self):
        # Add a user to test db temporary
        user1 = mixer.blend(User, id=1, first_name="Brad")
        assert User.objects.count() == 1

        # Get api url
        url1 = reverse("delete-user", kwargs={'pk': 1})
        url2 = reverse("delete-user", kwargs={'pk': 2})

        # call the url
        response1 = self.client.delete(url1)
        response2 = self.client.delete(url2)

        assert response1.json() is not None
        assert response1.status_code == 200
        assert response2.json() is not None
        assert response2.status_code == 400
        assert User.objects.count() == 0

    def test_login(self):
        user1 = mixer.blend(User, username="brad24", password=hash_password("123456"))
        assert User.objects.count() == 1

        input_data_1 = {
        }
        input_data_2 = {
            "username": "Ahmad"
        }
        input_data_3 = {
            "password": "Jalali"
        }
        input_data_4 = {
            "username": "Ahmad",
            "password": "Jalali"
        }
        input_data_5 = {
            "username": "brad24",
            "password": "Jalali"
        }
        input_data_6 = {
            "username": "Ahmad",
            "password": "123456"
        }
        input_data_7 = {
            "username": "brad24",
            "password": "123456"
        }

        # Get api url
        url = reverse("login")

        # call the url
        response1 = self.client.post(url, data=input_data_1)
        response2 = self.client.post(url, data=input_data_2)
        response3 = self.client.post(url, data=input_data_3)
        response4 = self.client.post(url, data=input_data_4)
        response5 = self.client.post(url, data=input_data_5)
        response6 = self.client.post(url, data=input_data_6)
        response7 = self.client.post(url, data=input_data_7)

        assert response1.json() is not None
        assert response2.json() is not None
        assert response3.json() is not None
        assert response4.json() is not None
        assert response5.json() is not None
        assert response6.json() is not None
        assert response7.json() is not None

        assert response1.status_code == 400
        assert response2.status_code == 400
        assert response3.status_code == 400
        assert response4.status_code == 400
        assert response5.status_code == 400
        assert response6.status_code == 400
        assert response7.status_code == 200

        assert response7.json()["username"] == "brad24"

    def test_update_user(self):
        user1 = mixer.blend(User, id=1, first_name="Hector", last_name="Williams")

        auth = Authenticate()
        token = auth.create_access_token(user1.id)

        input_data_1 = {
            "first_name": "Ahmad",
            "last_name": "Jalali"
        }
        input_data_2 = {
        }
        input_data_3 = {
            "last_name": "Jalali"
        }
        input_data_4 = {
            "first_name": "Ahmad"
        }

        # Get api url
        url = reverse("update-user")

        # call the url
        response0 = self.client.put(path=url, data=input_data_1, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiZXhwIjoxNjczMzQxNTkxLCJpYXQiOjE2NzMzMzc5OTF9.WIjYnNWRWR_Fo08Wluc344PesOkNewUaLmsCjGFYVvI")
        response00 = self.client.put(path=url, data=input_data_1, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="some-text")
        response000 = self.client.put(path=url, data=input_data_1, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZHMiOjMsImV4cCI6MTY3MzM0MTU5MSwiaWF0IjoxNjczMzM3OTkxfQ.tdqmMSqRogzcmP75kHIP640rdgHE2vbPyxaW_JhYivA")
        response0000 = self.client.put(path=url, data=input_data_1, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response1 = self.client.put(path=url, data=input_data_1, format="json")
        response2 = self.client.put(path=url, data=input_data_2, format="json")
        response3 = self.client.put(path=url, data=input_data_4, format="json")
        response4 = self.client.put(path=url, data=input_data_4, format="json")

        assert response0.json() is not None
        assert response0.status_code == 401

        assert response00.json() is not None
        assert response00.status_code == 401

        assert response000.json() is not None
        assert response000.status_code == 401

        assert response0000.json() is not None
        assert response0000.status_code == 401

        assert response1.json() is not None
        assert response1.status_code == 200
        assert response1.json()["first_name"] == "Ahmad"
        assert response1.json()["last_name"] == "Jalali"

        assert response2.json() is not None
        assert response2.status_code == 400

        assert response3.json() is not None
        assert response3.status_code == 400

        assert response4.json() is not None
        assert response4.status_code == 400
