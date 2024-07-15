from repositories.order_repository import OrderRepository


class ViewCartService:
    def __init__(self, conn) -> None:
        self.conn = conn
        self.order_repo = OrderRepository(conn)

    def view_cart(self, user_id: int) -> None:
        cart_items = self.order_repo.view_orders_from_cart(user_id)
        total_cost = sum(item[2] for item in cart_items)
        if cart_items:
            print("Товары в корзине:")
            for item in cart_items:
                # product = product_repo.find_by_name(item[2])
                print(f"{item[0]} - {item[1]} шт. - ${item[2]}")
            print(f"Итого: ${total_cost:.2f}")
        else:
            print("Корзина пуста.")
