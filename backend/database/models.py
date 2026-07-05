"""
Database models
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
import enum
from .database import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    NORMAL = "normal"
    ADMIN = "admin"
    EMPRESARIO = "empresario"  # Business owner role


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, values_callable=lambda x: [e.value for e in x]), 
                  default=UserRole.NORMAL, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
