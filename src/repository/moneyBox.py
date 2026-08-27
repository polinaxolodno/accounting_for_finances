from src.models.moneyBox import MoneyBox
from src.utils.repository import SQLAlchemyRepository


class MoneyBoxRepository(SQLAlchemyRepository):
    
    model = MoneyBox
