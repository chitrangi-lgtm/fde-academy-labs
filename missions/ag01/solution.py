from provided import *  # the client's code (the checker runs provided.py first)

def run_agent(task, model, tools, max_steps=6):
    history = [{"role": "user", "content": task}]
    while True:                                   # no step cap, no loop check, and any tool error crashes
        action = model(history)
        history.append({"role": "assistant", "content": action})
        if "final" in action:
            return {"answer": action["final"], "steps": len(history), "stopped": "final", "history": history}
        result = tools[action["tool"]](**action["args"])
        history.append({"role": "tool", "content": str(result)})


m = scripted({"tool": "lookup_order", "args": {"order_id": "A-1"}}, {"final": "Order A-1 has shipped."})
print(run_agent("Where is order A-1?", m, TOOLS))
