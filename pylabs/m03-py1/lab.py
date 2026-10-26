import duckdb
import pandas as pd

customers = pd.read_csv("customers.csv")
orders = pd.read_csv("orders.csv", parse_dates=["order_date"])

# DuckDB can query a DataFrame by its variable name:
print(duckdb.sql("SELECT COUNT(*) AS orders, SUM(amount) AS revenue FROM orders").df())

revenue_by_city = None   # DataFrame with columns city, revenue; highest revenue first; only cities with orders
no_orders = []           # names of customers with no orders, sorted
monthly = None           # DataFrame with columns month ('2026-01'), revenue, running_total; in month order
