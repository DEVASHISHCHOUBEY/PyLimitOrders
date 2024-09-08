import unittest
from unittest.mock import Mock
from limit.limit_order_agent import LimitOrderAgent

class LimitOrderAgentTest(unittest.TestCase):
    def setUp(self):
        self.mock_execution_client = Mock()
        self.agent = LimitOrderAgent(self.mock_execution_client)

    def test_basic_order_execution(self):
        # Add order before sending price tick
        self.agent.add_order(buy=True, product_id="IBM", amount=1000, limit=100.0)
        # Trigger price tick
        self.agent.on_price_tick("IBM", 99.0)
        # Check if buy method was called
        self.mock_execution_client.buy.assert_called_once_with("IBM", 1000)

    def test_add_order(self):
        self.agent.add_order(buy=True, product_id="AAPL", amount=500, limit=150.0)
        self.agent.on_price_tick("AAPL", 149.0)
        self.mock_execution_client.buy.assert_called_once_with("AAPL", 500)

        # Ensure that orders are cleared after execution
        self.agent.on_price_tick("AAPL", 149.0)
        self.mock_execution_client.buy.assert_called_once_with("AAPL", 500)  # Ensure it is only called once

    def test_sell_order(self):
        self.agent.add_order(buy=False, product_id="AAPL", amount=200, limit=155.0)
        self.agent.on_price_tick("AAPL", 156.0)
        self.mock_execution_client.sell.assert_called_once_with("AAPL", 200)

if _name_ == '_main_':
    unittest.main()

