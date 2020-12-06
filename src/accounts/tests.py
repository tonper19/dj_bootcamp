from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
# Create your tests here.

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        user_a = User(username="test_user", email="test_user@test.com")
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a_pw = "@test_password!"
        self.user_a_pw = user_a_pw
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a
        print(f"*** setUp: new test user: {user_a.id}-{user_a.username}")

    def test_001_user_exists(self):
        user_count = User.objects.all().count()
        print(f"*** _user_exists: user count: {user_count}")
        self.assertEqual(user_count, 1)

    def test_002_user_password(self):
        user_qs = User.objects.filter(username__iexact="test_user")
        user_exists = user_qs.exists() and user_qs.count() == 1
        print(f"*** _user_password: user_exists count: {user_qs.count()}")
        self.assertTrue(user_exists)
        print(f"*** _user_password: check password")
        user_a = User.objects.get(username="test_user")
        self.assertTrue(user_a.check_password(self.user_a_pw))

    def test_003_login_url(self):
        login_url = settings.LOGIN_URL
        data = {
            "username": self.user_a.username,
            "password": self.user_a.password,
        }
        print(f"*** _login_url: login")
        response = self.client.post(login_url, data, follow=True)
        # print(f"*** All response attributes: {dir(response)}")
        # print(f"*** All response.request attributes: {response.request}")
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")
        print(f"*** _login_url: redirect {redirect_path}")
        self.assertEqual(redirect_path, settings.LOGIN_URL)
        print(f"*** _login_url: status_code=200")
        self.assertEqual(status_code, 200)
