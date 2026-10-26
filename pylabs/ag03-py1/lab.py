import json
import re
from typing import Literal
from pydantic import BaseModel, Field, ValidationError

attempts = json.load(open("ticket_attempts.json"))   # the model's answers, in order (the second follows your retry message)

class Ticket(BaseModel):
    ticket_id: str
    priority: str
    summary: str
    category: str

def extract_json(text):
    """The first {...} object in the text, as a string."""
    return text

def retry_message(error):
    """A short instruction for the model naming every failing field (and the allowed values where there are some)."""
    return ""

final = None          # the first Ticket that validates
attempts_used = 0     # how many answers you needed
