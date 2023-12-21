users = []
# how to add  postgresql db
database: dict[int, dict[str]] = {}

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import ForeignKey, String, UniqueConstraint, BigInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, declarative_base

from config.config import load_config

config = load_config()
engine = create_async_engine(config.database.url, echo=True)
Base = declarative_base()


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

class Token(Base):
    __tablename__ = 'user_token'
    __table_args__ = (
        UniqueConstraint(
            'user_id',
            name='telegram_id_uniq'
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user_account.telegram_id', ondelete='CASCADE'),
    )

    ozon_admin_token = mapped_column(String, nullable=True)
    user: Mapped['User'] = relationship('User', back_populates='token')

async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
