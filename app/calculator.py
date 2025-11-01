import shlex
from .operations import create_operation
from .input_validators import two_numbers
from .calculation import Calculation
from .history import History, LoggingObserver, AutoSaveObserver
from .calculator_memento import Caretaker
from .exceptions import OperationError, ValidationError
from .logger import get_logger
from .calculator_config import cfg

log = get_logger("calculator")

class Calculator:
    def __init__(self):
        # Pass cfg into History so paths/flags track the current env
        self.history = History(cfg.MAX_HISTORY_SIZE, config=cfg)
        self.caretaker = Caretaker()
        self.history.register(LoggingObserver())
        self.history.register(AutoSaveObserver())

    def do_calc(self, op_name, a, b):
        a, b = two_numbers(a, b)
        op = create_operation(op_name)
        result = round(op.compute(a, b), cfg.PRECISION)
        # snapshot before mutating history
        self.caretaker.snapshot(self.history.list())
        calc = Calculation(op_name, a, b, result)
        self.history.add(calc)
        return result

    def undo(self):
        state, ok = self.caretaker.undo(self.history.list())
        if ok:
            self.history._items = state  # trusted internal swap
        return ok

    def redo(self):
        state, ok = self.caretaker.redo(self.history.list())
        if ok:
            self.history._items = state
        return ok

    def repl(self): # pragma: no cover
        print("Calculator REPL. Type 'help' for commands. 'exit' to quit.")
        while True:
            try:
                line = input("calc> ").strip()
                if not line: continue
                if line.lower() in ("exit","quit"): print("Bye."); break
                if line == "help":
                    print("Commands: add|subtract|multiply|divide|power|root|modulus|int_divide|percent|abs_diff a b")
                    print("history | clear | undo | redo | save | load | help | exit")
                    continue
                if line == "history":
                    for i, c in enumerate(self.history.list(), 1):
                        print(f"{i}. {c.operation}({c.a},{c.b})={c.result} [{c.timestamp}]")
                    continue
                if line == "clear":
                    self.caretaker.snapshot(self.history.list())
                    self.history.clear(); print("History cleared."); continue
                if line == "undo":
                    print("Undone." if self.undo() else "Nothing to undo."); continue
                if line == "redo":
                    print("Redone." if self.redo() else "Nothing to redo."); continue
                if line == "save":
                    self.history.save_to_csv(); print("Saved."); continue
                if line == "load":
                    self.history.load_from_csv(); print("Loaded."); continue

                parts = shlex.split(line)
                if len(parts) != 3:
                    print("Usage: <operation> <a> <b>"); continue
                op, a, b = parts
                res = self.do_calc(op, a, b)
                print(res)
            except (ValidationError, OperationError) as e:
                log.error(str(e)); print(f"Error: {e}")
            except KeyboardInterrupt:
                print("\nBye."); break
            except Exception as e:
                log.exception("Unhandled"); print(f"Fatal: {e}")
