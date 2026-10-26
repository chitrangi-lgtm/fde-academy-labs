import pandas as pd

raw = pd.read_csv("sales.csv")
print(raw)
print(raw.dtypes)

# The checks read these four names. Build them step by step and print as you go.
clean = raw          # duplicates removed, regions tidy, bad rows removed, plus a 'revenue' column (qty x unit_price)
bad_rows = 0         # how many rows you dropped because qty is missing or the date is not a real date
by_region = {}       # revenue per region, rounded to 2 decimals, e.g. {'North': 217.5, ...}
top_products = []    # product names, highest revenue first
