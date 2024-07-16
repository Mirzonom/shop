from typing import List, Tuple
from custom_sql_query import sql_query
from enums.sql_query_return_type import SqlQueryReturnType


class OrderRepository:
    def __init__(self, conn):
        self.conn = conn
        conn.execute('PRAGMA foreign_keys = ON')

    def create_table(self) -> None:
        sql_query(self.conn, '''
                        CREATE TABLE IF NOT EXISTS orders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            product_id INTEGER NOT NULL,
                            quantity INTEGER NOT NULL,
                            total_price REAL NOT NULL,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            status TEXT DEFAULT NULL,
                            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL, 
                            FOREIGN KEY (product_id) REFERENCES products(id)
                        )
                    ''')

    def create_order(self, user_id: int, product_id: int, quantity: int, total_price: float) -> int:
        return sql_query(self.conn, '''
            INSERT INTO orders (user_id, product_id, quantity, total_price) VALUES (?, ?, ?, ?)
            ''', (user_id, product_id, quantity, total_price), return_type=SqlQueryReturnType.LASTROWID)

    def find_by_user(self, user_id: int) -> list:
        return sql_query(self.conn, '''
            SELECT * FROM users WHERE id = ?
            ''', (user_id,), return_type=SqlQueryReturnType.FETCHALL)

    def check_my_orders_by_user_id(self, user_id: int) -> List[Tuple[int, str]]:
        return sql_query(self.conn, 'SELECT * FROM orders WHERE user_id=? AND status IS NULL',
                         (user_id,), return_type=SqlQueryReturnType.FETCHALL)

    def view_orders_from_cart(self, user_id: int) -> List[Tuple[str, int, float]]:
        return sql_query(self.conn, '''
            SELECT products.name, orders.quantity, orders.total_price
            FROM orders
            INNER JOIN products ON orders.product_id = products.id
            WHERE orders.user_id = ? AND orders.status IS NULL
            ''', (user_id,), return_type=SqlQueryReturnType.FETCHALL)

    def get_completed_orders(self, user_id: int) -> List[Tuple[str, int, float, str]]:
        return sql_query(self.conn, '''
            SELECT products.name, orders.quantity, orders.total_price, orders.timestamp
            FROM orders
            INNER JOIN products ON orders.product_id = products.id
            WHERE orders.user_id = ? AND orders.status = 'completed'
            ''', (user_id,), return_type=SqlQueryReturnType.FETCHALL)

    def update_status(self, order_id: int, status: str) -> None:
        sql_query(
            self.conn, '''UPDATE orders SET status = ? WHERE id = ?''', (status, order_id))

    def delete_orders_with_null_status(self) -> None:
        sql_query(self.conn, '''DELETE FROM orders WHERE status IS NULL''')

    # def update_orders_on_user_delete(self, user_id: int) -> None:
    #     sql_query(self.conn, '''UPDATE orders SET user_id = NULL WHERE user_id = ?
    #         ''', (user_id,))

    # def create_update_orders_trigger(self):
    #     sql_query(self.conn, '''
    #         CREATE TRIGGER IF NOT EXISTS update_orders_on_user_delete
    #         AFTER DELETE ON users
    #         FOR EACH ROW
    #         BEGIN
    #             UPDATE orders SET user_id = NULL WHERE user_id = OLD.id;
    #         END;
    #     ''')
