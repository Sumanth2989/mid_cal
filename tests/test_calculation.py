from app.calculation import Calculation

def test_calc_model():
    c = Calculation("add", 1, 2, 3)
    assert c.operation == "add" and c.result == 3
