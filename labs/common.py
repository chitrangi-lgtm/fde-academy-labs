"""Shared helpers for the Docker-tier labs: sample policy documents and a deterministic toy embedding.

The toy embedding (feature hashing of words) needs no model download or API key, so every lab runs offline. Swap
`embed` for a real embedding model in a client project; keep the dimension consistent across the collection.
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import Dict, List

DIM = 64

DOCS: List[Dict[str, str]] = [
    {"id": "POL-7.1", "tenant": "crestfin", "text": "Gold loan loan-to-value must not exceed 75% of the appraised gold value."},
    {"id": "POL-4.2", "tenant": "crestfin", "text": "Late payment interest is 2% per month on overdue small-business instalments."},
    {"id": "POL-2.9", "tenant": "crestfin", "text": "Small-business loans above $500,000 need approval from two credit officers."},
    {"id": "AMH-CL-3", "tenant": "albion", "text": "Physiotherapy claims need pre-authorisation before treatment starts."},
    {"id": "AMH-CL-8", "tenant": "albion", "text": "Oncology claims are always routed to clinical review."},
    {"id": "LKR-OPS-1", "tenant": "lakeshore", "text": "Hospital robots are only taken out of service after human confirmation."},
]


def embed(text: str) -> List[float]:
    vec = [0.0] * DIM
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        h = int(hashlib.sha256(word.encode()).hexdigest(), 16)
        vec[h % DIM] += 1.0 if (h >> 8) % 2 else -1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]
