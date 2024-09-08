from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = {}


    def add_order(self, buy: bool, product_id: str, amount: int, limit: float):
        if product_id not in self.orders:
            self.orders[product_id] = []
        self.orders[product_id].append({
            "buy": buy,
            "amount": amount,
            "limit": limit
        })

    def on_price_tick(self, product_id: str, price: float):
        if product_id in self.orders:
            for order in self.orders[product_id]:
                if (order["buy"] and price <= order["limit"]) or (not order["buy"] and price >= order["limit"]):
                    try:
                        if order["buy"]:
                            self.execution_client.buy(product_id, order["amount"])
                        else:
                            self.execution_client.sell(product_id, order["amount"])
                    except Exception as e:
                        print(f"Failed to execute order: {e}")
            # Remove executed orders
            self.orders[product_id] = [
                order for order in self.orders[product_id] 
                if not ((order["buy"] and price <= order["limit"]) or (not order["buy"] and price >= order["limit"]))
            ]