import json
import re
from typing import Literal
from pydantic import BaseModel, Field, ValidationError, model_validator

raw_outputs = json.load(open("model_outputs.json"))
for i, r in enumerate(raw_outputs):
    print(i, r[:90].replace("\n", " "), "...")

class Line(BaseModel):
    description: str
    qty: int
    unit_price: float

class Invoice(BaseModel):
    invoice_no: str
    currency: str
    lines: list[Line]
    total: float

def parse(raw: str) -> Invoice:
    """Validate one model output; pull the JSON out of chatty text first."""
    return Invoice.model_validate_json(raw)

valid, errors = [], {}   # invoice numbers that pass; {index: error message} for the ones that fail
