ROUTES = [("billing", ["refund", "charge", "invoice", "bill"]), ("technical", ["app", "login", "error", "crash"]),
          ("delivery", ["parcel", "courier", "delivery"])]


def billing(ticket):
    if "app" in ticket:
        return {"reply": "The charge looks right; the app problem is for technical.", "handoff": "technical"}
    return {"reply": "Refund approved.", "handoff": None}


def technical(ticket):
    if "charge" in ticket:
        return {"reply": "The app is fine; the charge is a billing question.", "handoff": "billing"}
    if "parcel" in ticket:
        return {"reply": "Login fixed; the parcel question is for delivery.", "handoff": "delivery"}
    return {"reply": "Please update the app.", "handoff": None}


def delivery(ticket):
    if "refund" in ticket:
        return {"reply": "Parcel found; refunds are billing's.", "handoff": "billing"}
    return {"reply": "Your parcel arrives tomorrow.", "handoff": None}


AGENTS = {"billing": billing, "technical": technical, "delivery": delivery}
