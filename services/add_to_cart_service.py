from repositories.product_repository import ProductRepository
from repositories.order_repository import OrderRepository


class AddToCartService:
    def __init__(self, conn) -> None:
        self.conn = conn
        self.product_repo = ProductRepository(conn)
        self.order_repo = OrderRepository(conn)

    def add_to_cart(self, user_id: int, product_id: int, quantity: int) -> None:
        virtual_quantity = self.product_repo.get_virtual_product_quantity(
            product_id)
        product = self.product_repo.find_by_id(product_id)

        if product and virtual_quantity >= quantity:  # проверяем наличие товара на складе
            total_price = product[2] * quantity
            self.order_repo.create_order(
                user_id, product_id, quantity, total_price)
            print(f"{quantity} единиц товара '{
                  product[1]}' добавлено в корзину.")
            # уменьшаем количество товара на складе
            new_stock = virtual_quantity - quantity
            self.product_repo.update_stock(product_id, new_stock, 0)
        else:
            print("Товар не найден или недостаточно на складе.")
