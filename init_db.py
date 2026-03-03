#!/usr/bin/env python3
"""
Initialize database with sample data for the Cosmetic Alena application
Run this script to populate the database with services and other data
"""

from app import app, db, Service, Appointment, ContactMessage, NewsletterSubscriber
from datetime import datetime, timedelta

def init_sample_data():
    """Initialize database with sample data"""
    
    print("Initializing database with sample data...")
    
    with app.app_context():
        # Clear existing data (optional)
        # db.drop_all()
        
        # Create tables
        db.create_all()
        
        # Check if services already exist
        if Service.query.count() > 0:
            print("✓ Services already exist in database")
        else:
            print("Adding sample services...")
            
            services = [
                Service(
                    name="Facial Treatment",
                    description="Professional European facial treatment with premium skincare products. Includes cleansing, exfoliation, extraction, massage, and hydrating mask.",
                    price=89.99,
                    duration=60,
                    category="Skincare",
                    image=None
                ),
                Service(
                    name="Makeup Application",
                    description="Professional makeup application for any occasion. Expert color matching and technique for a flawless finish.",
                    price=59.99,
                    duration=45,
                    category="Makeup",
                    image=None
                ),
                Service(
                    name="Hair Styling",
                    description="Precision hair cutting and professional styling. Includes consultation, cutting, and blow-dry styling.",
                    price=75.00,
                    duration=60,
                    category="Hair",
                    image=None
                ),
                Service(
                    name="Bridal Makeup",
                    description="Complete bridal makeup package with trial session. Long-lasting, professional wedding day makeup.",
                    price=150.00,
                    duration=90,
                    category="Makeup",
                    image=None
                ),
                Service(
                    name="Nail Art & Extensions",
                    description="Creative nail designs with gel polish or extensions. Professional application and cuticle care.",
                    price=65.00,
                    duration=90,
                    category="Nails",
                    image=None
                ),
                Service(
                    name="Eyebrow Threading",
                    description="Precise eyebrow shaping and threading. Includes tinting for a polished look.",
                    price=25.00,
                    duration=30,
                    category="Grooming",
                    image=None
                ),
                Service(
                    name="Deep Cleansing Peel",
                    description="Chemical peel treatment for skin renewal and brightening. Improves skin texture and tone.",
                    price=120.00,
                    duration=75,
                    category="Skincare",
                    image=None
                ),
                Service(
                    name="Relaxation Massage",
                    description="Full body relaxation massage. Swedish massage techniques to relieve tension and stress.",
                    price=99.99,
                    duration=60,
                    category="Wellness",
                    image=None
                ),
                Service(
                    name="Eyelash Extensions",
                    description="Luxurious eyelash extensions application. Adds volume and length for a dramatic look.",
                    price=110.00,
                    duration=120,
                    category="Makeup",
                    image=None
                ),
                Service(
                    name="Hair Coloring",
                    description="Professional hair coloring service. Root touch-up, full color, highlights, or balayage.",
                    price=95.00,
                    duration=90,
                    category="Hair",
                    image=None
                ),
                Service(
                    name="Body Treatment",
                    description="Luxurious body scrub and hydration treatment. Includes exfoliation and moisturizing application.",
                    price=85.00,
                    duration=60,
                    category="Wellness",
                    image=None
                ),
                Service(
                    name="Waxing Services",
                    description="Professional waxing for hair removal. Available for face, legs, arms, and other areas.",
                    price=45.00,
                    duration=45,
                    category="Grooming",
                    image=None
                ),
            ]
            
            for service in services:
                db.session.add(service)
            
            db.session.commit()
            print(f"✓ Added {len(services)} sample services")
        
        # Add sample newsletter subscribers (optional)
        if NewsletterSubscriber.query.count() == 0:
            print("Adding sample subscribers...")
            
            subscribers = [
                NewsletterSubscriber(
                    email="john@example.com",
                    name="John Doe"
                ),
                NewsletterSubscriber(
                    email="jane@example.com",
                    name="Jane Smith"
                ),
            ]
            
            for subscriber in subscribers:
                db.session.add(subscriber)
            
            db.session.commit()
            print(f"✓ Added {len(subscribers)} sample subscribers")
        
        print("\n✓ Database initialization complete!")
        print("\nSample Data Summary:")
        print(f"  - Services: {Service.query.count()}")
        print(f"  - Appointments: {Appointment.query.count()}")
        print(f"  - Contact Messages: {ContactMessage.query.count()}")
        print(f"  - Newsletter Subscribers: {NewsletterSubscriber.query.count()}")

if __name__ == '__main__':
    init_sample_data()
    print("\nYou can now run the application:")
    print("  python3 app.py")
    print("\nThen visit: http://localhost:5000")
