from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UUID, Index, TIMESTAMP, func
from src.db.session import Base
import uuid
from src.schema.user import UserOutPutModel
from datetime import datetime


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        Index('idx_email', 'email'),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[String] = mapped_column(String, nullable=False)
    email: Mapped[String] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[String] = mapped_column(String, nullable=False)
    date_joined: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    def serialize(self) -> UserOutPutModel:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "date_joined": self.date_joined
        }

    money_boxes = relationship("MoneyBox", back_populates="user")
    daily_budget = relationship("DailyBudget", back_populates="user")
