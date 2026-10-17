import pytest

from src.services.dailyBudget import _calculate_daily_budget, days_left
from fastapi import HTTPException

def test_calculate_daily_budget():
    assert _calculate_daily_budget(5, 1000) == 200
    assert _calculate_daily_budget(2, 666) == 333
    assert _calculate_daily_budget(3, 100) == pytest.approx(33.33, abs=0.01)

def test_calculate_daily_budget_exception():
    with pytest.raises(HTTPException, match="Дата за периодом") as status_code:
        _calculate_daily_budget(0, 1000)
    assert status_code.value.status_code == 400

@pytest.mark.parametrize("days", [0, -1, -3, -4, -100])
def test_negative_calculate_daily_budget(days):
    with pytest.raises(HTTPException, match="Дата за периодом"):
        _calculate_daily_budget(days, 1000)

@pytest.mark.parametrize("days, total_budget, expected", [
    (2, 100, 50),
    (1, 1000, 1000),
    (3, 100, 33.33),
    (5, 0, 0),
    (365, 1_000_000, 2739.73),
], ids=["обычный случай", "последний день", "копейки", "пустой бюджет", "год с большим бюджетом"])
def test_calculate_daily_budget_precalculated(days, total_budget, expected):
    assert _calculate_daily_budget(days, total_budget) == pytest.approx(expected, abs=0.01)
