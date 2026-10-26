import pandas as pd
from scipy.stats import binomtest, fisher_exact

runs = pd.read_csv("eval_runs.csv")
print(runs.sum(numeric_only=True))

b = 0            # tasks the old prompt failed and the new prompt passed
c = 0            # tasks the old prompt passed and the new prompt failed
p_paired = 1.0   # McNemar's exact test: a two-sided binomial test of c successes in b + c trials, p = 0.5
p_unpaired = 1.0 # Fisher's exact test on [[new passes, new fails], [old passes, old fails]], ignoring the pairing
decision = ""    # 'ship' if p_paired < 0.05, otherwise 'hold'
