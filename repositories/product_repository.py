from typing import Optional, List, Tuple
from custom_sql_query import sql_query
from enums.sql_query_return_type import SqlQueryReturnType
from enums.transaction_type import TransactionType


class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self) -> None:
        sql_query(self.conn, '''
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        price REAL NOT NULL,
                        category_id INTEGER NOT NULL,
                        stock INTEGER DEFAULT 0,
                        FOREIGN KEY (category_id) REFERENCES categories(id)
                    )
                ''')

    def create_product(self, name: str, price: float, category_id: int, stock: int) -> int:
        return sql_query(self.conn, '''
            INSERT INTO products (name, price, category_id, stock) VALUES (?, ?, ?, ?)
            ''', (name, price, category_id, stock), return_type=SqlQueryReturnType.LASTROWID)

    def find_by_id(self, product_id: int) -> Optional[tuple]:
        return sql_query(self.conn, '''
            SELECT * FROM products WHERE id = ?
            ''', (product_id,), return_type=SqlQueryReturnType.FETCHONE)

    def find_by_name(self, name: str) -> Optional[tuple]:
        return sql_query(self.conn, '''
            SELECT * FROM products WHERE name = ?
        ''', (name,), return_type=SqlQueryReturnType.FETCHONE)

    def get_products_by_category(self, category_name: str) -> List[Tuple[int, str, float, int]]:
        return sql_query(self.conn, '''
                SELECT products.id, products.name, products.price, products.stock
                FROM products
                JOIN categories ON products.category_id = categories.id
                WHERE categories.name = ? AND products.stock > 0
            ''', (category_name,), return_type=SqlQueryReturnType.FETCHALL)

    def get_products_by_category_id(self, category_id) -> List[Tuple[int, str, float, int]]:
        return sql_query(self.conn, '''
                SELECT id, name, price, stock
                FROM products
                WHERE category_id = ? AND stock > 0
            ''', (category_id,), return_type=SqlQueryReturnType.FETCHALL)

    def update_stock(self, product_id: int, new_stock: int, transaction_type: int) -> None:
        sql_query(self.conn, '''
            UPDATE products SET stock = ? WHERE id = ?
            ''', (new_stock, product_id))

    def get_virtual_product_quantity(self, product_id: int) -> int:
        transactions = sql_query(self.conn, "SELECT quantity, type FROM product_transactions WHERE product_id = ?",
                                 (product_id,), return_type=SqlQueryReturnType.FETCHALL)
        # исходный stock из таблицы products
        total_quantity = self.find_by_id(product_id)[4]
        for quantity, transaction_type in transactions:
            if transaction_type == TransactionType.Withdrawal:  # списание
                total_quantity -= quantity
            elif transaction_type == TransactionType.Deposit:  # зачисление
                total_quantity += quantity
        return total_quantity
