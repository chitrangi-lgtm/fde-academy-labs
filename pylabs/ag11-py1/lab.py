import pandas as pd

calls = pd.read_csv("calls.csv")
# dollars per million tokens: (input, cached input, output)
PRICES = {"flash-lite": (0.10, 0.025, 0.40), "flash": (0.30, 0.075, 2.50), "pro": (1.25, 0.3125, 10.00)}
print(calls.head())

by_feature = {}      # dollars per feature for the week, rounded to 2 decimals
spike_day = ""       # the day with the highest total cost
spike_feature = ""   # the feature that cost the most on that day
cache_hit_rate = 0.0 # cached input tokens / all input tokens, for the week
