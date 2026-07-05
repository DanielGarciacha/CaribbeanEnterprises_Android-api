"""
Database models
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
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

    # Relationships
    reviews = relationship("Review", back_populates="user")
    business = relationship("Business", back_populates="owner", uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"


class Business(Base):
    """Business/Company model"""
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    about = Column(Text, nullable=True)
    address = Column(String(255), nullable=True)
    phone_number = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    website = Column(String(200), nullable=True)
    category = Column(String(100), nullable=True)
    tag = Column(String(50), nullable=True)          # e.g. "Popular", "Nuevo"
    rating = Column(Float, default=0.0)
    image_url = Column(String(500), nullable=True)   # URL de imagen principal
    logo_url = Column(String(500), nullable=True)    # URL del logo
    hero_url = Column(String(500), nullable=True)    # URL de imagen hero/banner
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    owner = relationship("User", back_populates="business")
    products = relationship("Product", back_populates="business", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="business", cascade="all, delete-orphan")
    gallery = relationship("BusinessGallery", back_populates="business", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Business(id={self.id}, name='{self.name}')>"


class BusinessGallery(Base):
    """Gallery images for a Business"""
    __tablename__ = "business_gallery"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    image_url = Column(String(500), nullable=False)

    business = relationship("Business", back_populates="gallery")


class Product(Base):
    """Product model belonging to a Business"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    full_description = Column(Text, nullable=True)
    price = Column(String(100), nullable=True)
    image_url = Column(String(500), nullable=True)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    business = relationship("Business", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}')>"


class Review(Base):
    """Customer review for a Business"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="reviews")
    business = relationship("Business", back_populates="reviews")

    def __repr__(self):
        return f"<Review(id={self.id}, rating={self.rating})>"
