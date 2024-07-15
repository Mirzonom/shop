import sqlite3

from database import OrderRepository, ProductRepository, UserRepository, TransactionRepository

conn = sqlite3.connect('shop.db')
order_repo = OrderRepository(conn)
product_repo = ProductRepository(conn)
user_repo = UserRepository(conn)
transaction_repo = TransactionRepository(conn)


def add_to_cart(user_id: int, product_id: int, quantity: int) -> None:
    virtual_quantity = product_repo.get_virtual_product_quantity(product_id)
    product = product_repo.find_by_id(product_id)

    if product and virtual_quantity >= quantity:  # проверяем наличие товара на складе
        total_price = product[2] * quantity
        order_repo.create_order(user_id, product_id, quantity, total_price)
        print(f"{quantity} единиц товара '{product[1]}' добавлено в корзину.")
        # уменьшаем количество товара на складе
        new_stock = virtual_quantity - quantity
        product_repo.update_stock(product_id, new_stock, 0)
    else:
        print("Товар не найден или недостаточно на складе.")


def view_cart(user_id: int) -> None:
    cart_items = order_repo.view_orders_from_cart(user_id)
    total_cost = sum(item[2] for item in cart_items)
    if cart_items:
        print("Товары в корзине:")
        for item in cart_items:
            # product = product_repo.find_by_name(item[2])
            print(f"{item[0]} - {item[1]} шт. - ${item[2]}")
        print(f"Итого: ${total_cost:.2f}")
    else:
        print("Корзина пуста.")


def checkout(user_id: int) -> None:
    orders = order_repo.check_my_orders_by_user_id(user_id)
    if not orders:
        return print("Корзина пуста.")

    total_cost = sum(order[4] for order in orders)

    user_balance = user_repo.get_virtual_balance(user_id)

    # if user_balance is None:
    #     print(f"Пользователь с id={user_id} не найден.")
    #     return

    if total_cost > user_balance:
        print("Недостаточно средств на балансе.")
        return

    confirmation: str = input(f"Для оплаты заказа будет снято ${total_cost:.2f}. Вы подтверждаете? (Ok/No): ")

    if confirmation.lower() == 'ok':
        transaction_repo.add_money_transaction(user_id, total_cost, 0)
        # new_balance = user_balance - total_cost
        # user_repo.update_balance(user_id, new_balance)

        for order in orders:
            order_repo.update_status(order[0], 'completed')

        print("\nЧек:")
        for order in orders:
            product = product_repo.find_by_id(order[2])
            if product:
                print(f"{product[1]} - ${order[4]}")
            else:
                print(f"Товар с id={order[2]} не найден.")
        print(f"Итого: ${total_cost:.2f}")
        print(f"Ваш текущий баланс: {user_balance - total_cost:.2f}")
    else:
        print("Оплата отменена.")


def purchase_history(user_id: int) -> None:
    completed_orders = order_repo.get_completed_orders(user_id)
    if completed_orders:
        print("История покупок:")
        for order in completed_orders:
            print(f"{order[3]} - {order[0]} - {order[1]} шт. - ${order[2]:.2f}")
    else:
        print("У вас пока нет покупок.")
