from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str | None]
