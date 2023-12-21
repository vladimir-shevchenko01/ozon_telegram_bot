
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base

if TYPE_CHECKING:
    from database.models.token import Token


class User(Base):
     __tablename__: str = 'user_account'

     id: Mapped[int] = mapped_column(primary_key=True)
     telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
     token: Mapped['Token'] = relationship(
         'Token',
         back_populates='user',
         cascade='all, delete',
         passive_deletes=True,
     )

