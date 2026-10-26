import sqlite3


def load(conn):
    """Create and fill the tables from shop.sql."""


def revenue_by_region(conn):
    return []


def customers_without_orders(conn):
    return []


def orders_for(conn, name):
    return []


conn = sqlite3.connect(":memory:")
load(conn)
print(revenue_by_region(conn))
