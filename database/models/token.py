from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base

if TYPE_CHECKING:
    from database.models.user import User


class Token(Base):
    __tablename__ = 'user_token'
    __table_args__ = (
        UniqueConstraint(
            'telegram_id',
            name='telegram_id_uniq'
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user_account.telegram_id', ondelete='CASCADE'),
    )

    ozon_admin_token = mapped_column(String, nullable=True)
    user: Mapped['User'] = relationship('User', back_populates='token')