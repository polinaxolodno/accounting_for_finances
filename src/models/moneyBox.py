from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UUID, Float, ForeignKey, Index, CheckConstraint
from src.db.session import Base
import uuid
from src.schema.moneyBox import MoneyBoxOutPutModel


class MoneyBox(Base):
    __tablename__ = 'money_box'
    __table_args__ = (
        Index('idx_moneybox_user', 'userid', 'moneyboxname'),
        CheckConstraint('moneyboxname IS NOT NULL', 'row monebox_name is not null'),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    moneyboxname: Mapped[String] = mapped_column(String, nullable=False)
    userid: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('user.id'), nullable=False)
    moneygoal: Mapped[Float] = mapped_column(Float, default=0, nullable=False)
    moneybudget: Mapped[Float] = mapped_column(Float, default=0, nullable=False)

    def serialize(self) -> MoneyBoxOutPutModel:
        return {
            "id": self.id,
            "moneyboxname": self.moneyboxname,
            "userid": self.userid,
            "moneygoal": self.moneygoal,
            "moneybudget": self.moneybudget
        }

    # связь между таблиц. (название таблицы, куда соединяется не совпадает с названием класса)
    user = relationship("User", back_populates="money_boxes")
