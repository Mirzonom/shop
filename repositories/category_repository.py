from typing import Optional, List, Tuple
from custom_sql_query import sql_query
from enums.sql_query_return_type import SqlQueryReturnType


class CategoryRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self) -> None:
        sql_query(self.conn, '''
                        CREATE TABLE IF NOT EXISTS categories (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL UNIQUE
                        )
                    ''')

    def create_category(self, name: str) -> int:
        return sql_query(self.conn, '''
            INSERT INTO categories (name) VALUES (?)
            ''', (name,), return_type=SqlQueryReturnType.LASTROWID)

    def find_by_name(self, name: str) -> Optional[tuple]:
        return sql_query(self.conn, '''
                SELECT * FROM categories WHERE name = ?
                    ''', (name,), return_type=SqlQueryReturnType.FETCHONE)

    def get_all_categories(self) -> List[Tuple[int, str]]:
        return sql_query(self.conn, 'SELECT id, name FROM categories', return_type=SqlQueryReturnType.FETCHALL)
