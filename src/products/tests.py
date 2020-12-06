from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Product
# Create your tests here.
User = get_user_model()


class ProductTestCase(TestCase):
    def setUp(self):
        print(f"*** ProductTestCase setUp")
        user_a = User(username="staff_user", email="test_user@test.com")
        user_a.is_staff = True
        user_a.is_superuser = False
        user_a_pw = "@test_password!"
        self.user_a_pw = user_a_pw
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

        user_b = User(username="regular_user", email="test_user2@test.com")
        user_b.is_staff = True
        user_b.is_superuser = False
        user_b_pw = "@test_password!"
        self.user_b_pw = user_b_pw
        user_b.set_password(user_b_pw)
        user_b.save()

        self.user_b = user_b

    def test_001_user_count(self):
        print(f"*** ProductTestCase _user_count")
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)

    def test_002_invalid_request(self):
        print(f"*** ProductTestCase _invalid_request")
        is_logged_in = self.client.login(username=self.user_b.username,
                                         password=self.user_b_pw
                                         )
        response = self.client.post(
            "/products/create/",
            {
                "title": "user is not a staff member should not be allowed to enter this"
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_003_valid_request(self):
        print(f"*** ProductTestCase _valid_request")
        is_logged_in = self.client.login(username=self.user_a.username,
                                         password=self.user_a_pw
                                         )
        response = self.client.post(
            "/products/create/",
            {
                "title": "user is a staff member should be allowed to enter this"
            }
        )
        self.assertEqual(response.status_code, 200)
