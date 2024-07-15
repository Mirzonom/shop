from enum import Enum


class SqlQueryReturnType(Enum):
    FETCHALL = 'fetchall'
    FETCHONE = 'fetchone'
    LASTROWID = 'lastrowid'
