import os
import pytest
from importlib import reload

def _fresh_calculator(tmp_path, extra_env=None):
    """
    Fresh Calculator bound to per-test tmp dirs.
    Returns (calculator, cfg).
    """
    os.environ["CALCULATOR_HISTORY_DIR"] = str(tmp_path / "history")
    os.environ["CALCULATOR_LOG_DIR"] = str(tmp_path / "logs")
    if extra_env:
        for k, v in extra_env.items():
            os.environ[k] = str(v)

    import app.calculator_config as cc
    reload(cc)
    import app.input_validators as iv
    reload(iv)
    import app.calculator as calc_mod
    reload(calc_mod)

    from app.calculator import Calculator
    return Calculator(), cc.cfg


def test_do_calc_add(tmp_path):
    calc, _ = _fresh_calculator(tmp_path)
    res = calc.do_calc("add", "2", "3")
    assert res == 5.0


def test_validation_max(tmp_path):
    # Clamp max input to 10 so 999 should fail validation
    calc, _ = _fresh_calculator(tmp_path, {"CALCULATOR_MAX_INPUT_VALUE": "10"})
    from app.exceptions import ValidationError
    with pytest.raises(ValidationError):
        calc.do_calc("add", "999", "1")


def test_calculator_happy_flow(tmp_path):
    c, _ = _fresh_calculator(tmp_path)
    assert c.do_calc("add", "2", "3") == 5.0
    assert c.do_calc("multiply", 4, 2) == 8.0
    assert len(c.history.list()) == 2


def test_calculator_error_paths(tmp_path):
    c, _ = _fresh_calculator(tmp_path)
    from app.exceptions import OperationError
    with pytest.raises(OperationError):
        c.do_calc("not_an_op", 1, 2)
    with pytest.raises(OperationError):
        c.do_calc("divide", 1, 0)
    with pytest.raises(OperationError):
        c.do_calc("root", -8, 2)  # even root of negative


def test_root_negative_odd_is_ok(tmp_path):
    c, _ = _fresh_calculator(tmp_path)
    assert c.do_calc("root", -8, 3) == -2.0  # cube root


def test_undo_redo_and_clear(tmp_path):
    c, _ = _fresh_calculator(tmp_path)
    c.do_calc("add", 1, 1)
    c.do_calc("add", 2, 2)
    assert len(c.history.list()) == 2

    assert c.undo() is True
    assert len(c.history.list()) == 1

    assert c.redo() is True
    assert len(c.history.list()) == 2

    # nothing more to redo
    assert c.redo() in (False, 0)

    # clear with snapshot
    c.caretaker.snapshot(c.history.list())
    c.history.clear()
    assert len(c.history.list()) == 0


def test_autosave_and_load(tmp_path):
    c, cfg = _fresh_calculator(tmp_path, {"CALCULATOR_AUTO_SAVE": "true"})
    c.do_calc("add", 5, 7)  # triggers AutoSaveObserver
    csv_path = os.path.join(cfg.HISTORY_DIR, "history.csv")
    assert os.path.exists(csv_path)

    # load into a fresh instance
    c2, _ = _fresh_calculator(tmp_path)
    c2.history.load_from_csv()
    items = c2.history.list()
    assert len(items) == 1 and items[0].result == 12.0
