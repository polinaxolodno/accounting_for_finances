from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, UUID, Boolean
from src.db.session import Base
import uuid

class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[String] = mapped_column(String, nullable=False)
    email: Mapped[String] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[String] = mapped_column(String, nullable=False)