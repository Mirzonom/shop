from repositories.order_repository import OrderRepository


class PurchaseHistoryService:
    def __init__(self, conn) -> None:
        self.conn = conn
        self.order_repo = OrderRepository(conn)

    def purchase_history(self, user_id: int) -> None:
        completed_orders = self.order_repo.get_completed_orders(user_id)
        if completed_orders:
            print("История покупок:")
            for order in completed_orders:
                print(f"{order[3]} - {order[0]} - {order[1]
                                                   } шт. - ${order[2]:.2f}")
        else:
            print("У вас пока нет покупок.")
