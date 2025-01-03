from pgvector.sqlalchemy import Vector
from pydantic import EmailStr
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    Session,
    declarative_base,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import select

from app.utils import get_brazil_time

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    uuid: Mapped[UUID] = mapped_column(UUID, primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    nickname: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[EmailStr] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=get_brazil_time)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=get_brazil_time, onupdate=get_brazil_time)
    activated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=get_brazil_time, onupdate=get_brazil_time)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    roles: Mapped[JSON] = mapped_column(JSON, default={})
    embeddings: Mapped[list['Embeddings']] = relationship('Embeddings', back_populates='user')

    @classmethod
    def find_by_email(cls, db: Session, email: str):
        query = select(cls).where(cls.email == email)
        result = db.execute(query)
        user = result.scalars().first()
        return user

class Embeddings(Base):
    __tablename__ = 'embeddings'
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.uuid'), nullable=False
    )
    embedding: Mapped[Vector] = mapped_column(Vector, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=get_brazil_time
    )
    user: Mapped['User'] = relationship('User', back_populates='embeddings')
