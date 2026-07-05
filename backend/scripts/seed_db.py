"""
Database Seeding Script
Populates the database with initial businesses, products, and reviews
"""
import sys
import os
import random
from datetime import datetime

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import engine, SessionLocal
from database.models import User, Business, Product, Review, BusinessGallery, UserRole
from auth import get_password_hash

def seed_database():
    db = SessionLocal()
    try:
        print("🌱 Seeding the database...")
        
        # 1. Create a business owner if it doesn't exist
        owner = db.query(User).filter(User.username == "empresario_demo").first()
        if not owner:
            owner = User(
                username="empresario_demo",
                email="empresario_demo@test.com",
                hashed_password=get_password_hash("123456"),
                role=UserRole.EMPRESARIO
            )
            db.add(owner)
            db.commit()
            db.refresh(owner)
            print("👤 Created demo business owner")

        # 2. Create normal users for reviews
        reviewers = []
        for i in range(1, 4):
            r = db.query(User).filter(User.username == f"cliente{i}").first()
            if not r:
                r = User(
                    username=f"cliente{i}",
                    email=f"cliente{i}@test.com",
                    hashed_password=get_password_hash("123456"),
                    role=UserRole.NORMAL
                )
                db.add(r)
                db.commit()
                db.refresh(r)
            reviewers.append(r)

        # 3. Create Businesses
        businesses_data = [
            {
                "name": "La Pizzería del Centro",
                "description": "Auténtica pizza italiana a la leña",
                "about": "Fundada en 2010, traemos el sabor de Nápoles directamente a tu paladar. Utilizamos ingredientes frescos y locales combinados con quesos importados de alta calidad.",
                "address": "Calle Principal #123, Centro",
                "phone_number": "+1234567890",
                "email": "contacto@pizzeriacentro.com",
                "website": "www.pizzeriacentro.com",
                "category": "Restaurante",
                "tag": "Popular",
                "rating": 4.8,
                "image_url": "pizza", # Use local drawable names as discussed
                "logo_url": "pizza_logo",
                "hero_url": "pizza_hero"
            },
            {
                "name": "TechStore Express",
                "description": "La mejor tecnología al mejor precio",
                "about": "Somos líderes en venta de gadgets, smartphones y computadoras. Brindamos garantía y soporte técnico garantizado.",
                "address": "Avenida Tecnológica #456",
                "phone_number": "+0987654321",
                "email": "ventas@techstore.com",
                "website": "www.techstore.com",
                "category": "Tecnología",
                "tag": "Nuevo",
                "rating": 4.5,
                "image_url": "tech",
                "logo_url": "tech_logo",
                "hero_url": "tech_hero"
            },
            {
                "name": "Café Aroma",
                "description": "El mejor inicio para tus mañanas",
                "about": "Granos 100% orgánicos cultivados a más de 1200 metros de altura. Especialistas en filtrados y repostería artesanal.",
                "address": "Plaza Central, Local 4",
                "phone_number": "+1122334455",
                "email": "hola@cafearoma.com",
                "website": "www.cafearoma.com",
                "category": "Cafetería",
                "tag": "Recomendado",
                "rating": 4.9,
                "image_url": "cafe",
                "logo_url": "cafe_logo",
                "hero_url": "cafe_hero"
            }
        ]

        # Ensure we don't duplicate businesses
        if db.query(Business).count() == 0:
            for b_data in businesses_data:
                business = Business(
                    owner_id=owner.id,
                    **b_data
                )
                db.add(business)
                db.commit()
                db.refresh(business)
                print(f"🏢 Created business: {business.name}")

                # Create Products for each business
                for i in range(1, 4):
                    product = Product(
                        name=f"Producto Estrella {i} - {business.name[:5]}",
                        description=f"Un excelente producto de {business.name}",
                        full_description=f"Esta es una descripción más larga y detallada del producto {i}. Incluye todas sus características, especificaciones y por qué deberías comprarlo hoy mismo.",
                        price=f"${random.randint(10, 100)}.99",
                        image_url=business.image_url, # Reutilizar imagen para el mockup
                        rating=random.uniform(3.5, 5.0),
                        review_count=random.randint(5, 50),
                        business_id=business.id
                    )
                    db.add(product)
                
                # Create Reviews for each business
                for r_user in reviewers:
                    review = Review(
                        rating=random.randint(3, 5),
                        comment=random.choice([
                            "¡Excelente servicio, muy recomendado!",
                            "Buena calidad pero el tiempo de espera fue un poco largo.",
                            "Me encantó, definitivamente volveré pronto.",
                            "Los mejores de la zona sin duda alguna."
                        ]),
                        user_id=r_user.id,
                        business_id=business.id
                    )
                    db.add(review)
                
                db.commit()

            print("✅ Database successfully seeded with Businesses, Products, and Reviews!")
        else:
            print("⚠️ Database already contains businesses. Skipping seeding to avoid duplicates.")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
