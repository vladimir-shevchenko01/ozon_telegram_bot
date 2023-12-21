from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
