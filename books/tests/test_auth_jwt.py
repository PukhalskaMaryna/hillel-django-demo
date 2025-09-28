from django.test import TestCase, Client
from django.contrib.auth import get_user_model
import json

class JWTAuthBasicTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        User.objects.create_user(username="tester", password="pass12345")

    def test_can_get_tokens(self):
        resp = self.client.post(
            "/api/token/",
            data=json.dumps({"username": "tester", "password": "pass12345"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        data = resp.json()
        self.assertIn("access", data)
        self.assertIn("refresh", data)
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

class JWTAuthProtectedTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_protected_requires_auth(self):
        resp = self.client.get("/api/hello/")
        assert resp.status_code in (401, 403), resp.status_code
from django.test import TestCase, Client
import json

class JWTAuthWithAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        # створюємо користувача
        from django.contrib.auth import get_user_model
        get_user_model().objects.create_user(username="tester", password="pass12345")

    def test_protected_with_access_ok(self):
        # беремо access
        r = self.client.post("/api/token/",
                             data=json.dumps({"username": "tester", "password": "pass12345"}),
                             content_type="application/json")
        access = r.json()["access"]
        # перевіряємо захищений ендпоінт
        r2 = self.client.get("/api/hello/", HTTP_AUTHORIZATION=f"Bearer {access}")
        assert r2.status_code == 200, r2.status_code
        assert "hello" in r2.json()
from django.test import TestCase, Client
import json
from django.contrib.auth import get_user_model

class JWTAuthRefreshTests(TestCase):
    def setUp(self):
        self.client = Client()
        get_user_model().objects.create_user(username="tester", password="pass12345")

    def test_can_refresh_access(self):
        r = self.client.post("/api/token/",
                             data=json.dumps({"username": "tester", "password": "pass12345"}),
                             content_type="application/json")
        refresh = r.json()["refresh"]
        r2 = self.client.post("/api/token/refresh/",
                              data=json.dumps({"refresh": refresh}),
                              content_type="application/json")
        assert r2.status_code == 200, r2.status_code
        assert "access" in r2.json()
from django.test import TestCase, Client
import json

class JWTAuthBadCredsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_bad_credentials(self):
        r = self.client.post(
            "/api/token/",
            data=json.dumps({"username": "nouser", "password": "nope"}),
            content_type="application/json",
        )
        assert r.status_code in (400, 401), r.status_code
from django.test import TestCase, Client
import json
from django.contrib.auth import get_user_model

class HelloPayloadTests(TestCase):
    def setUp(self):
        self.client = Client()
        get_user_model().objects.create_user(username="tester", password="pass12345")

    def test_hello_returns_username(self):
        r = self.client.post("/api/token/",
                             data=json.dumps({"username": "tester", "password": "pass12345"}),
                             content_type="application/json")
        access = r.json()["access"]
        r2 = self.client.get("/api/hello/", HTTP_AUTHORIZATION=f"Bearer {access}")
        assert r2.status_code == 200
        assert r2.json().get("hello") == "tester"
