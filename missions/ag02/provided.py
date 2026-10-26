REFUNDS = []

REGISTRY = {
    "create_refund": {
        "schema": {"type": "object", "additionalProperties": False, "required": ["order_id", "amount", "currency"],
                   "properties": {"order_id": {"type": "string", "pattern": "ORD-[0-9]{6}"},
                                  "amount": {"type": "number", "minimum": 0.01, "maximum": 500},
                                  "currency": {"type": "string", "enum": ["USD", "EUR", "GBP"]},
                                  "note": {"type": "string"}}},
        "needs_approval": lambda args: args["amount"] > 100,
        "fn": lambda order_id, amount, currency, note="": REFUNDS.append((order_id, amount)) or f"refund {order_id} queued",
    },
    "lookup_order": {
        "schema": {"type": "object", "required": ["order_id"], "properties": {"order_id": {"type": "string"}}},
        "needs_approval": lambda args: False,
        "fn": lambda order_id: f"{order_id}: delivered",
    },
}
