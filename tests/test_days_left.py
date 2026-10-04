import pytest
from datetime import datetime
from src.services.dailyBudget import days_left

def test_days_left():
    assert days_left(datetime(2026, 10, 10)) == 6