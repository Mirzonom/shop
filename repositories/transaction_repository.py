from custom_sql_query import sql_query


class TransactionRepository:
    def __init__(self, conn):
        self.conn = conn
        conn.execute('PRAGMA foreign_keys = ON')

    def create_table_money_transaction(self) -> None:
        sql_query(self.conn, '''
                    CREATE TABLE IF NOT EXISTS money_transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        amount REAL NOT NULL,
                        type INTEGER NOT NULL, -- 0 для списания, 1 для зачисления
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
                    )
                ''')

    def create_table_quantity_transaction(self) -> None:
        sql_query(self.conn, '''
                            CREATE TABLE IF NOT EXISTS product_transactions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                product_id INTEGER NOT NULL,
                                quantity INTEGER NOT NULL,
                                type INTEGER NOT NULL, -- 0 для списания, 1 для зачисления
                                FOREIGN KEY (product_id) REFERENCES products(id)
                            )
                        ''')

    def add_money_transaction(self, user_id: int, amount: float, transaction_type: int) -> None:
        sql_query(self.conn, '''
            INSERT INTO money_transactions (user_id, amount, type) VALUES (?, ?, ?)
        ''', (user_id, amount, transaction_type))

    def add_product_quantity_transaction(self, product_id: int, quantity: int, transaction_type: int) -> None:
        sql_query(self.conn, '''
            INSERT INTO product_transactions (product_id, quantity, type) VALUES (?, ?, ?)
        ''', (product_id, quantity, transaction_type))

    # def update_money_transactions_on_user_delete(self, user_id: int) -> None:
    #     sql_query(self.conn, '''
    #         UPDATE money_transactions SET user_id = NULL WHERE user_id = ?
    #     ''', (user_id,))

    # def create_update_transactions_trigger(self):
    #     sql_query(self.conn, '''
    #         CREATE TRIGGER IF NOT EXISTS update_transactions_on_user_delete
    #         AFTER DELETE ON users
    #         FOR EACH ROW
    #         BEGIN
    #             UPDATE money_transactions SET user_id = NULL WHERE user_id = OLD.id;
    #         END;
    #     ''')
