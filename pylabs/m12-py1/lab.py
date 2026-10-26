import pandas as pd

a = pd.read_csv("supplier_a.csv", dtype=str)
b = pd.read_csv("supplier_b.csv", dtype=str)
c = pd.read_csv("supplier_c.csv", dtype=str)
for name, df in [("a", a), ("b", b), ("c", c)]:
    print(name, list(df.columns))
    print(df, end="\n\n")

clean = pd.DataFrame(columns=["supplier", "sku", "price", "updated"])   # sku 'AB-100', price float, updated 'YYYY-MM-DD'
quarantine = []   # one {'supplier': 'a', 'row': 2, 'reason': 'bad price' or 'missing sku'} per rejected row
