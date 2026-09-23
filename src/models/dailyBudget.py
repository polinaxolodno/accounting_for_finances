from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UUID, Index, TIMESTAMP, Float,  ForeignKey, func
from src.db.session import Base
import uuid
from src.schema.dailyBudget import DailyBudgetOutPutModel
from datetime import datetime


class DailyBudget(Base):
    __tablename__ = "dailyBudget"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    budget: Mapped[Float] = mapped_column(Float, nullable=False)
    date_end: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    userid: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('user.id'), nullable=False)
    def serialize(self) -> DailyBudgetOutPutModel:
        return {
            "id": self.id,
            "budget": self.budget,
            "date_end": self.date_end,
            "userid": self.userid
        }

    user = relationship("User", back_populates="daily_budget")
