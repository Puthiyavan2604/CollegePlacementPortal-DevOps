
import os
import tempfile
import unittest
from pathlib import Path

from app import app


class PortalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.original_db = app.config.get("TEST_DATABASE_PATH")

        # Give each test its own clean database.
        app.config["TEST_DATABASE_PATH"] = (
            Path(self.tmp.name) / "test.db"
        )

        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        if self.original_db is None:
            app.config.pop("TEST_DATABASE_PATH", None)
        else:
            app.config["TEST_DATABASE_PATH"] = self.original_db

        self.tmp.cleanup()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CampusConnect", response.data)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "healthy")

    def test_job(self):
        self.assertEqual(self.client.get("/jobs/1").status_code, 200)

    def test_unknown_job(self):
        self.assertEqual(self.client.get("/jobs/999").status_code, 404)

    def test_apply(self):
        response = self.client.post(
            "/apply/1",
            data={
                "full_name": "Test Student",
                "email": "test@example.com",
                "department": "Computer Science and Engineering",
                "graduation_year": "2027",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Application Received", response.data)


if __name__ == "__main__":
    unittest.main()
