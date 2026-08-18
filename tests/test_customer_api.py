import unittest

from fastapi.testclient import TestClient

from app.api.server import app


class CustomerApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_chat_balance(self):
        response = self.client.post("/api/chat", json={"message": "查询余额"})
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["intent"], "balance")
        self.assertTrue(body["success"])


if __name__ == "__main__":
    unittest.main()
