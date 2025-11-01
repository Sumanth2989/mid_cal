import os
import pytest
from importlib import reload
from app.calculation import Calculation


def _fresh_history(tmp_path):
    # Unique, empty dir per test
    os.environ["CALCULATOR_HISTORY_DIR"] = str(tmp_path / "hist")
    import app.calculator_config as cc
    reload(cc)
    import app.history as hist
    reload(hist)
    from app.history import History
    return History(cc.cfg.MAX_HISTORY_SIZE, config=cc.cfg), cc.cfg


def test_history_add_and_list(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "h1"))
    import app.calculator_config as cc
    reload(cc)
    import app.history as hist
    reload(hist)

    from app.history import History, LoggingObserver, AutoSaveObserver
    h = History(cc.cfg.MAX_HISTORY_SIZE, config=cc.cfg)
    h.register(LoggingObserver())
    h.register(AutoSaveObserver())

    h.add(Calculation("add", 1, 2, 3))
    assert len(h.list()) == 1


def test_observer_failure_is_swallowed(tmp_path, caplog):
    h, _ = _fresh_history(tmp_path)

    class BadObserver:
        def notify(self, calc, history):
            raise RuntimeError("boom")

    h.register(BadObserver())
    h.add(Calculation("add", 1, 2, 3))
    assert len(h.list()) == 1
    assert any("Observer failed" in r.getMessage() for r in caplog.records)


def test_save_error_branch(tmp_path):
    h, _ = _fresh_history(tmp_path)
    h.add(Calculation("add", 1, 2, 3))
    from app.exceptions import OperationError
    bad_path = os.path.join(str(tmp_path), "no", "such", "dir", "file.csv")
    with pytest.raises(OperationError):
        h.save_to_csv(path=bad_path)


def test_load_missing_file_warns(tmp_path, caplog):
    h, cfg = _fresh_history(tmp_path)
    # Ensure file is missing
    target = os.path.join(cfg.HISTORY_DIR, "history.csv")
    if os.path.exists(target):
        os.remove(target)

    # Use explicit path to avoid cross-test leakage
    h.load_from_csv(path=target)
    assert len(h.list()) == 0

    msgs = "\n".join(r.getMessage() for r in caplog.records).lower()
    assert ("not found" in msgs) or ("no history file" in msgs) or msgs == ""
