import unittest

from app.agent.customer_agent import route_intent, handle_customer_query
from app.tools.customer_tools import query_balance


class CustomerAgentTests(unittest.TestCase):
    def test_route_intent_balance(self):
        self.assertEqual(route_intent("我的余额还剩多少"), "balance")

    def test_route_intent_order(self):
        self.assertEqual(route_intent("我想查一下订单"), "order")

    def test_route_intent_unknown(self):
        self.assertEqual(route_intent("今天的天气怎么样"), "unknown")

    def test_query_balance_returns_structured_result(self):
        result = query_balance("13863727112")
        self.assertTrue(result["success"])
        self.assertIn("余额", result["message"])

    def test_handle_customer_query_balance(self):
        result = handle_customer_query("查询余额")
        self.assertEqual(result["intent"], "balance")
        self.assertTrue(result["success"])

    def test_handle_customer_query_knowledge_lookup(self):
        result = handle_customer_query("退款会多久到账")
        self.assertIn(result["intent"], ["knowledge", "unknown"])
        self.assertTrue(result["success"])
        self.assertTrue(bool(result["data"]))


if __name__ == "__main__":
    unittest.main()
