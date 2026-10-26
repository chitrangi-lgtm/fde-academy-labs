def scripted(*actions):
    """A stand-in model: replies with these actions in order, then repeats the last one."""
    actions = list(actions)

    def model(history):
        done = sum(1 for h in history if h["role"] == "assistant")
        return actions[min(done, len(actions) - 1)]
    return model


TOOLS = {
    "lookup_order": lambda order_id: {"A-1": "shipped", "A-2": "processing"}.get(order_id, "not found"),
    "refund_status": lambda order_id: "refund issued" if order_id == "A-1" else "no refund",
}
