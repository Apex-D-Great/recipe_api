import unittest
from backend.config import TestConfig
from backend import app
from backend.models import db

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client(self)
        with self.app.app_context():
            db.create_all()

    def test_signup(self):
        signup_resp = self.client.post(
            "/auth/signup",
            json={
                "username":"dayo1",
                "email":"dayo1@gmail.com",
                "password":"password"
            }
        )
        status_code = signup_resp.status_code
        self.assertEqual(status_code, 201)

    def test_login(self):
        signup_resp = self.client.post(
            "/auth/signup",
            json={
                "username":"dayo1",
                "email":"dayo1@gmail.com",
                "password":"password"
            }
        )
        login_resp = self.client.post(
            "/auth/login",
            json={
                "email":"dayo1@gmail.com",
                "password":"password"
            }
        )
        access_token=login_resp.json["message"]
        print(access_token)
        status_code = login_resp.status_code
        self.assertEqual(status_code, 200)

    def test_recipe(self):
        signup_resp = self.client.post(
            "/auth/signup",
            json={
                "username":"dayo1",
                "email":"dayo1@gmail.com",
                "password":"password"
            }
        )
        login_resp = self.client.post(
            "/auth/login",
            json={
                "email":"dayo1@gmail.com",
                "password":"password"
            }
        )

        access_token=login_resp.json["access_token"]
        print(access_token)

        recipe_resp = self.client.post(
            "/recipe/recipes",
            json={
                "title":"dayo1",
                "description":"dayo1@gmail.com"
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )

        recipes_resp = self.client.get(
            "/recipe/recipes",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        print(recipes_resp.json)
        status_code = recipe_resp.status_code
        self.assertEqual(status_code, 201)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()