from src.schema.dailyBudget import DailyBudgetCreate
import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from datetime import datetime

def test_daily_budget_create_types():
    with pytest.raises(ValidationError) as e:
        DailyBudgetCreate(total_budget = "hggjhg", date_end= "yidsu", userid="hkb")
    assert {error["loc"][0] for error in e.value.errors()} == {"total_budget", "date_end", "userid"}