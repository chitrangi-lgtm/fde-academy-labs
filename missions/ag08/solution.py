from provided import *  # the client's code (the checker runs provided.py first)

import json


def handle(text):
    msg = json.loads(text)
    return json.dumps({"jsonrpc": "2.0", "id": msg["id"], "result": {}})


print(handle('{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}'))
