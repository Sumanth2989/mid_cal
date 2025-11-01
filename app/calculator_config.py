import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def _bool(val, default=False):
    if val is None: return default
    return str(val).strip().lower() in ("1", "true", "yes", "y", "on")

@dataclass(frozen=True)
class Config:
    LOG_DIR: str = os.getenv("CALCULATOR_LOG_DIR", "logs")
    HISTORY_DIR: str = os.getenv("CALCULATOR_HISTORY_DIR", "history")
    HISTORY_FILE: str = os.path.join(os.getenv("CALCULATOR_HISTORY_DIR", "history"), "history.csv")
    MAX_HISTORY_SIZE: int = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "1000"))
    AUTO_SAVE: bool = _bool(os.getenv("CALCULATOR_AUTO_SAVE", "true"))
    PRECISION: int = int(os.getenv("CALCULATOR_PRECISION", "6"))
    MAX_INPUT_VALUE: float = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e9"))
    DEFAULT_ENCODING: str = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

cfg = Config()
