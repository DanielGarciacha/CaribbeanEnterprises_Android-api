"""
Business, Product, Review, Admin, and Dashboard routers
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from database.database import get_db
from database.models import Business, Product, Review, User, UserRole
from schemas.business_schemas import (
    BusinessListResponse,
    BusinessDetailResponse,
    ProductResponse,
    ReviewResponse,
    ReviewCreate,
    AdminStatsResponse,
    BusinessDashboardResponse
)
from auth.auth import get_current_user

# Routers
business_router = APIRouter(prefix="/businesses", tags=["Businesses"])
admin_router = APIRouter(prefix="/admin", tags=["Admin"])
dashboard_router = APIRouter(prefix="/business", tags=["Business Dashboard"])

# --- Business Endpoints ---

@business_router.get("", response_model=List[BusinessListResponse])
async def get_businesses(db: Session = Depends(get_db)):
    """Get all businesses"""
    businesses = db.query(Business).all()
    return businesses

@business_router.get("/{business_id}", response_model=BusinessDetailResponse)
async def get_business_detail(business_id: int, db: Session = Depends(get_db)):
    """Get business details including products, reviews, and gallery"""
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # We populate username manually for reviews
    for review in business.reviews:
        review.username = review.user.username
        
    return business

@business_router.get("/{business_id}/products", response_model=List[ProductResponse])
async def get_business_products(business_id: int, db: Session = Depends(get_db)):
    """Get products for a specific business"""
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business.products

@business_router.post("/{business_id}/reviews", response_model=ReviewResponse)
async def create_review(
    business_id: int, 
    review: ReviewCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a review for a business (Requires Authentication)"""
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
        
    new_review = Review(
        rating=review.rating,
        comment=review.comment,
        user_id=current_user.id,
        business_id=business_id
    )
    db.add(new_review)
    
    # Update business rating
    total_reviews = db.query(Review).filter(Review.business_id == business_id).count()
    current_rating = business.rating or 0.0
    new_rating = ((current_rating * total_reviews) + review.rating) / (total_reviews + 1)
    business.rating = new_rating
    
    db.commit()
    db.refresh(new_review)
    
    # Set username manually for response
    new_review.username = current_user.username
    
    return new_review

# --- Admin Endpoints ---

@admin_router.get("/stats", response_model=AdminStatsResponse)
async def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get statistics for the admin dashboard"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized, admin only")
        
    total_users = db.query(User).count()
    total_companies = db.query(Business).count()
    total_products = db.query(Product).count()
    total_reviews = db.query(Review).count()
    
    return AdminStatsResponse(
        total_users=total_users,
        total_companies=total_companies,
        total_products=total_products,
        total_reviews=total_reviews
    )

# --- Business Dashboard Endpoints ---

@dashboard_router.get("/dashboard", response_model=BusinessDashboardResponse)
async def get_business_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard metrics for the authenticated business owner"""
    if current_user.role != UserRole.EMPRESARIO:
        raise HTTPException(status_code=403, detail="Not authorized, business owners only")
        
    business = db.query(Business).filter(Business.owner_id == current_user.id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found for this user")
        
    total_reviews = db.query(Review).filter(Review.business_id == business.id).count()
    total_products = db.query(Product).filter(Product.business_id == business.id).count()
    
    # Get recent reviews
    recent_reviews = db.query(Review).filter(
        Review.business_id == business.id
    ).order_by(Review.created_at.desc()).limit(5).all()
    
    for r in recent_reviews:
        r.username = r.user.username
    
    return BusinessDashboardResponse(
        business_name=business.name,
        owner_name=current_user.username,
        total_reviews=total_reviews,
        average_rating=business.rating or 0.0,
        total_products=total_products,
        recent_reviews=recent_reviews
    )
