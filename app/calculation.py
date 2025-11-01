from dataclasses import dataclass
from datetime import datetime

@dataclass
class Calculation:
    operation: str
    a: float
    b: float
    result: float
    timestamp: str = datetime.utcnow().isoformat()
