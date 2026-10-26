import json

PLAN = json.load(open("plan.json"))
TASKS, DEPS = PLAN["tasks"], PLAN["depends_on"]


def waves(tasks, depends_on):
    return [sorted(tasks)]


def has_cycle(tasks, depends_on):
    return False


def critical_path(tasks, depends_on):
    return [], 0
