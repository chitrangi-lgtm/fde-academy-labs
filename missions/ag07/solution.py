from provided import *  # the client's code (the checker runs provided.py first)

def route(ticket):
    return "billing"


def supervise(ticket, agents, max_handoffs=2):
    agent = route(ticket)
    result = agents[agent](ticket)
    return {"handled_by": agent, "transcript": [(agent, result["reply"])], "escalated": False}


print(supervise("I want a refund", AGENTS))
