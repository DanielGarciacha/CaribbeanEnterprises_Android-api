"""
Business, Product and Review schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ---- Gallery ----
class GalleryImageResponse(BaseModel):
    id: int
    image_url: str
    class Config:
        from_attributes = True


# ---- Product ----
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    full_description: Optional[str] = None
    price: Optional[str] = None
    image_url: Optional[str] = None
    rating: float = 0.0
    review_count: int = 0
    business_id: int

    class Config:
        from_attributes = True


# ---- Review ----
class ReviewCreate(BaseModel):
    rating: float
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    rating: float
    comment: Optional[str] = None
    user_id: int
    business_id: int
    created_at: datetime
    username: Optional[str] = None  # populated manually

    class Config:
        from_attributes = True


# ---- Business ----
class BusinessListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    tag: Optional[str] = None
    rating: float = 0.0
    image_url: Optional[str] = None
    logo_url: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True


class BusinessDetailResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    about: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    category: Optional[str] = None
    tag: Optional[str] = None
    rating: float = 0.0
    image_url: Optional[str] = None
    logo_url: Optional[str] = None
    hero_url: Optional[str] = None
    products: List[ProductResponse] = []
    reviews: List[ReviewResponse] = []
    gallery: List[GalleryImageResponse] = []

    class Config:
        from_attributes = True


# ---- Admin Stats ----
class AdminStatsResponse(BaseModel):
    total_users: int
    total_companies: int
    total_products: int
    total_reviews: int


# ---- Business Dashboard ----
class BusinessDashboardResponse(BaseModel):
    business_name: str
    owner_name: str
    total_reviews: int
    average_rating: float
    total_products: int
    recent_reviews: List[ReviewResponse] = []
