import json
import networkx as nx

plan = json.load(open("plan.json"))
print(plan)

G = nx.DiGraph()   # add one edge per dependency: prerequisite -> task

batches = []          # tasks that can run together, wave by wave; each wave sorted by name
critical_path = []    # the chain of tasks that takes longest
duration = 0          # its length in days (sum of the task durations)

def has_cycle(extra_edges):
    """Would adding these (from, to) edges make the plan impossible?"""
    return False
