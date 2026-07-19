from django.test import TestCase
from django.urls import reverse


class UserAuthenticationTests(TestCase):
    def test_google_login_page_is_available(self):
        response = self.client.get(reverse("users:login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "로그인하기")

    def test_local_signup_route_does_not_exist(self):
        response = self.client.get("/signup/")

        self.assertEqual(response.status_code, 404)

    def test_allauth_local_account_routes_do_not_exist(self):
        self.assertEqual(self.client.get("/accounts/login/").status_code, 404)
        self.assertEqual(self.client.get("/accounts/signup/").status_code, 404)
