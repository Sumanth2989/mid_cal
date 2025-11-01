import os
import pandas as pd
from typing import List, Protocol, Optional
from .calculation import Calculation
from .calculator_config import cfg as default_cfg
from .exceptions import OperationError
from .logger import get_logger

log = get_logger("history")


class Observer(Protocol):
    def notify(self, calculation: Calculation, history: "History") -> None: ...


class LoggingObserver:
    def notify(self, calculation: Calculation, history: "History") -> None:
        log.info(
            "CALC: %s(%s, %s) = %s",
            calculation.operation,
            calculation.a,
            calculation.b,
            calculation.result,
        )


class AutoSaveObserver:
    def notify(self, calculation: Calculation, history: "History") -> None:
        # Use the history's *current* cfg, not a module-level cfg snapshot
        if getattr(history, "cfg", default_cfg).AUTO_SAVE:
            history.save_to_csv()


class History:
    def __init__(self, max_size: int, config: Optional[object] = None):
        """
        max_size: max number of items to keep
        config: pass calculator_config.cfg here so paths follow the current env
        """
        self.cfg = config or default_cfg
        self._items: List[Calculation] = []
        self._observers: List[Observer] = []
        os.makedirs(self.cfg.HISTORY_DIR, exist_ok=True)

        # Optional housekeeping: ensure parent dir of file exists too
        file_dir = os.path.dirname(self.cfg.HISTORY_FILE)
        if file_dir:
            os.makedirs(file_dir, exist_ok=True)

        self.max_size = max_size

    def add(self, calc: Calculation):
        self._items.append(calc)
        if len(self._items) > self.max_size:
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
            return pd.DataFrame(columns=["operation", "a", "b", "result", "timestamp"])
        # Avoid relying on __dict__ shape; be explicit
        return pd.DataFrame(
            {
                "operation": [c.operation for c in self._items],
                "a": [c.a for c in self._items],
                "b": [c.b for c in self._items],
                "result": [c.result for c in self._items],
                "timestamp": [getattr(c, "timestamp", "") for c in self._items],
            }
        )

    def save_to_csv(self, path: Optional[str] = None):
        try:
            df = self.to_dataframe()
            out = path or self.cfg.HISTORY_FILE
            # Ensure directory exists if a custom path was passed
            os.makedirs(os.path.dirname(out) or self.cfg.HISTORY_DIR, exist_ok=True)
            df.to_csv(out, index=False, encoding=self.cfg.DEFAULT_ENCODING)
            log.info("History saved to %s", out)
        except Exception as e:
            raise OperationError(f"Failed to save history: {e}") from e

    def load_from_csv(self, path: Optional[str] = None):
        from .calculation import Calculation  # local import to avoid cycles
        src = path or self.cfg.HISTORY_FILE
        if not os.path.exists(src):
            log.warning("History file not found: %s", src)
            return
        try:
            df = pd.read_csv(src, encoding=self.cfg.DEFAULT_ENCODING)
            self._items.clear()
            for _, row in df.iterrows():
                self._items.append(
                    Calculation(
                        operation=row["operation"],
                        a=float(row["a"]),
                        b=float(row["b"]),
                        result=float(row["result"]),
                        timestamp=str(row.get("timestamp", "")),
                    )
                )
            log.info("History loaded from %s", src)
        except Exception as e:
            raise OperationError(f"Failed to load history: {e}") from e
