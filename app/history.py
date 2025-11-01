import os
import pandas as pd
from typing import List, Protocol
from .calculation import Calculation
from .calculator_config import cfg
from .exceptions import OperationError
from .logger import get_logger

log = get_logger("history")

class Observer(Protocol):
    def notify(self, calculation: Calculation, history: "History") -> None: ...

class LoggingObserver:
    def notify(self, calculation: Calculation, history: "History") -> None:
        log.info("CALC: %s(%s, %s) = %s", calculation.operation, calculation.a, calculation.b, calculation.result)

class AutoSaveObserver:
    def notify(self, calculation: Calculation, history: "History") -> None:
        if cfg.AUTO_SAVE:
            history.save_to_csv()

class History:
    def __init__(self, max_size: int):
        self._items: List[Calculation] = []
        self._observers: List[Observer] = []
        os.makedirs(cfg.HISTORY_DIR, exist_ok=True)

    def add(self, calc: Calculation):
        self._items.append(calc)
        if len(self._items) > cfg.MAX_HISTORY_SIZE:
            self._items.pop(0)
        self._broadcast(calc)

    def clear(self):
        self._items.clear()

    def list(self) -> List[Calculation]:
        return list(self._items)

    def register(self, obs: Observer):
        self._observers.append(obs)

    def _broadcast(self, calc: Calculation):
        for obs in self._observers:
            try:
                obs.notify(calc, self)
            except Exception as e:
                log.error("Observer failed: %s", e)

    def to_dataframe(self) -> pd.DataFrame:
        if not self._items:
            return pd.DataFrame(columns=["operation","a","b","result","timestamp"])
        return pd.DataFrame([c.__dict__ for c in self._items])

    def save_to_csv(self, path: str = None):
        try:
            df = self.to_dataframe()
            path = path or cfg.HISTORY_FILE
            df.to_csv(path, index=False, encoding=cfg.DEFAULT_ENCODING)
            log.info("History saved to %s", path)
        except Exception as e:
            raise OperationError(f"Failed to save history: {e}") from e

    def load_from_csv(self, path: str = None):
        from .calculation import Calculation
        path = path or cfg.HISTORY_FILE
        if not os.path.exists(path):
            log.warning("History file not found: %s", path)
            return
        try:
            df = pd.read_csv(path, encoding=cfg.DEFAULT_ENCODING)
            self._items.clear()
            for _, row in df.iterrows():
                self._items.append(Calculation(
                    operation=row["operation"],
                    a=float(row["a"]), b=float(row["b"]),
                    result=float(row["result"]),
                    timestamp=str(row.get("timestamp",""))
                ))
            log.info("History loaded from %s", path)
        except Exception as e:
            raise OperationError(f"Failed to load history: {e}") from e
