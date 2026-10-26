import json
from jsonschema import Draft202012Validator

data = json.load(open("tool_calls.json"))
schema, calls = data["schema"], data["calls"]
print(json.dumps(schema, indent=1))

def check_call(args):
    """Return (True, '') if args are valid, else (False, field) naming the field at fault."""
    return True, ""

report = []            # one {'index': i, 'valid': bool, 'field': str} per call, in order
safe_to_execute = []   # indexes of the calls that may run
