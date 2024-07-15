from typing import Optional
from custom_sql_query import sql_query
from enums.sql_query_return_type import SqlQueryReturnType
from enums.transaction_type import TransactionType


class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self) -> None:
        sql_query(self.conn, '''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    )
                ''')

    def create_user(self, username: str, password: str) -> int:
        return sql_query(self.conn, '''
                        INSERT INTO users (username, password) VALUES (?, ?)
                    ''', (username, password), return_type=SqlQueryReturnType.LASTROWID)

    def find_by_username(self, username: str) -> Optional[tuple]:
        return sql_query(self.conn, '''
                        SELECT * FROM users WHERE username = ?
                    ''', (username,), return_type=SqlQueryReturnType.FETCHONE)

    def get_virtual_balance(self, user_id: int) -> float:
        transactions = sql_query(self.conn, "SELECT amount, type FROM money_transactions WHERE user_id = ?",
                                 (user_id,), return_type=SqlQueryReturnType.FETCHALL)
        total_balance = 1000.0  # начальный баланс
        for amount, transaction_type in transactions:
            if transaction_type == TransactionType.Withdrawal:  # списание
                total_balance -= amount
            elif transaction_type == TransactionType.Deposit:  # зачисление
                total_balance += amount
        return total_balance

    def delete_user(self, user_id: int) -> None:
        sql_query(self.conn, '''
                DELETE FROM users WHERE id = ?
            ''', (user_id,))
