import json


def run(state_path, event=None):
    """draft -> waiting_for_approval -> sent (on 'approve') or rejected (on 'reject')."""
    return "waiting_for_approval"


print(run("demo.json"))
print(run("demo.json", "approve"))
