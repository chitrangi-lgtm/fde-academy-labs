import pandas as pd
import matplotlib.pyplot as plt

base = {"benefit": 420_000, "upfront": 600_000, "run": 80_000}

def npv(benefit, upfront, run, years=3, rate=0.10):
    """Net present value: minus the upfront cost, plus each year's (benefit - run) discounted to today."""
    return 0.0

sensitivity = {}   # {'benefit': (npv with benefit 20% lower, npv with it 20% higher), 'upfront': ..., 'run': ...}
ranking = []       # drivers ordered by swing (high minus low, in absolute value), largest first
# Then draw a tornado chart: one horizontal bar per driver, spanning low to high NPV.
