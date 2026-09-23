from src.models.dailyBudget import DailyBudget
from src.utils.repository import SQLAlchemyRepository


class DailyBudgetRepository(SQLAlchemyRepository):
    
    model = DailyBudget
