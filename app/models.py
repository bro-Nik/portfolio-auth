from typing import List, Optional
from datetime import datetime, timezone

from app.schemas.user import UserRole
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, Enum, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    token: Mapped[str] = mapped_column(String(512), unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(BigInteger, nullable=False)

    # Связи
    user: Mapped['User'] = relationship('User', back_populates='refresh_tokens')


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name='user_role', values_callable=lambda obj: [e.value for e in obj]),
        default=UserRole.USER,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_active_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Связи
    refresh_tokens: Mapped[List['RefreshToken']] = relationship(
        'RefreshToken',
        back_populates='user',
        cascade='all, delete-orphan'
    )
