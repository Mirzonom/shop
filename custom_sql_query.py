from typing import Any
from enums.sql_query_return_type import SqlQueryReturnType


def sql_query(conn, query: str, params: tuple = (), return_type: str = SqlQueryReturnType.LASTROWID) -> Any:
    with conn:
        cursor = conn.cursor()
        cursor.execute(query, params)

        if return_type == SqlQueryReturnType.FETCHALL:
            return cursor.fetchall()
        elif return_type == SqlQueryReturnType.FETCHONE:
            return cursor.fetchone()
        return cursor.lastrowid
