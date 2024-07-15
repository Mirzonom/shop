from repositories.order_repository import OrderRepository
from repositories.user_repository import UserRepository
from repositories.transaction_repository import TransactionRepository
from repositories.product_repository import ProductRepository


class CheckoutService:
    def __init__(self, conn) -> None:
        self.conn = conn
        self.order_repo = OrderRepository(conn)
        self.user_repo = UserRepository(conn)
        self.transaction_repo = TransactionRepository(conn)
        self.product_repo = ProductRepository(conn)

    def checkout(self, user_id: int) -> None:
        orders = self.order_repo.check_my_orders_by_user_id(user_id)
        if not orders:
            return print("Корзина пуста.")

        total_cost = sum(order[4] for order in orders)

        user_balance = self.user_repo.get_virtual_balance(user_id)

        # if user_balance is None:
        #     print(f"Пользователь с id={user_id} не найден.")
        #     return

        if total_cost > user_balance:
            print("Недостаточно средств на балансе.")
            return

        confirmation: str = input(f"Для оплаты заказа будет снято ${
            total_cost:.2f}. Вы подтверждаете? (Ok/No): ")

        if confirmation.lower() == 'ok':
            self.transaction_repo.add_money_transaction(user_id, total_cost, 0)
            # new_balance = user_balance - total_cost
            # user_repo.update_balance(user_id, new_balance)

            for order in orders:
                self.order_repo.update_status(order[0], 'completed')

            print("\nЧек:")
            for order in orders:
                product = self.product_repo.find_by_id(order[2])
                if product:
                    print(f"{product[1]} - ${order[4]}")
                else:
                    print(f"Товар с id={order[2]} не найден.")
            print(f"Итого: ${total_cost:.2f}")
            print(f"Ваш текущий баланс: {user_balance - total_cost:.2f}")
        else:
            print("Оплата отменена.")
