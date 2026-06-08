"""User model for known identities."""

from sqlalchemy import Column, Integer, String

from app.database.db import Base


class User(Base):
    """Known person enrolled in the face recognition system."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=True, unique=True)
    role = Column(String, default="member")
