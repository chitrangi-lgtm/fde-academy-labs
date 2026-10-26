import csv

with open("prices.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row)


def current_prices(path):
    """{SKU: today's price} for every SKU in the file."""
    return {}


def conflicts(path):
    """Sorted SKUs whose latest effective date has more than one distinct price."""
    return []
