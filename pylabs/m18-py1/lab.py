import pandas as pd
import matplotlib.pyplot as plt

traces = pd.read_csv("traces.csv")
print(traces.head(10))

p95 = {}            # {'auth': 59.6, ...}: each span's 95th percentile in ms, rounded to 1 decimal
slowest_span = ""   # the span with the highest p95
slow_traces = []    # trace ids whose spans add up to more than 2500 ms, sorted
# Then draw a bar chart of p95 by span.
