"""
Seed Data Generator
Generates realistic sample data for demo purposes
"""

from datetime import datetime, timedelta
import random
from app import db
from models.store import Store, StoreMetrics, FunnelStage, Recommendation

def generate_sample_data():
    """Generate sample data for the demo store"""
    
    # Create demo store if not exists
    demo_store = Store.query.filter_by(name='UrbanThreads').first()
    if not demo_store:
        demo_store = Store(
            name='UrbanThreads',
            platform='shopify',
            url='urbanthreads-demo.myshopify.com',
            annual_revenue=2300000,
            monthly_visitors=45000,
            conversion_rate=5.46,
            aov=78,
            ltv=156,
            tier='scale',
            is_active=True,
            is_connected=True,
            connected_at=datetime.utcnow() - timedelta(days=90)
        )
        db.session.add(demo_store)
        db.session.commit()
    
    # Generate 90 days of metrics
    base_date = datetime.utcnow() - timedelta(days=90)
    
    for i in range(90):
        date = base_date + timedelta(days=i)
        
        # Add some seasonality and trends
        day_of_week = date.weekday()
        weekend_factor = 1.3 if day_of_week >= 5 else 1.0
        trend_factor = 1 + (i * 0.002)  # 0.2% daily growth
        random_factor = random.uniform(0.9, 1.1)
        
        # Base metrics
        base_visitors = 1500
        visitors = int(base_visitors * weekend_factor * trend_factor * random_factor)
        
        # Conversion funnel
        product_views = int(visitors * 0.50)
        add_to_carts = int(product_views * 0.30)
        checkouts = int(add_to_carts * 0.60)
        orders = int(checkouts * 0.607)
        
        # Revenue
        aov = 78 + random.uniform(-5, 5)
        revenue = round(orders * aov, 2)
        
        # Traffic sources
        traffic_sources = {
            'organic': int(visitors * 0.35),
            'paid': int(visitors * 0.25),
            'social': int(visitors * 0.20),
            'email': int(visitors * 0.15),
            'direct': int(visitors * 0.05)
        }
        
        # Device breakdown
        device_breakdown = {
            'desktop': int(visitors * 0.40),
            'mobile': int(visitors * 0.50),
            'tablet': int(visitors * 0.10)
        }
        
        metrics = StoreMetrics(
            store_id=demo_store.id,
            date=date.date(),
            sessions=visitors,
            unique_visitors=int(visitors * 0.85),
            page_views=int(visitors * 3.2),
            bounce_rate=round(random.uniform(35, 45), 2),
            avg_session_duration=int(random.uniform(120, 180)),
            add_to_carts=add_to_carts,
            checkouts=checkouts,
            orders=orders,
            revenue=revenue,
            cart_conversion_rate=round((add_to_carts / product_views) * 100, 2) if product_views > 0 else 0,
            checkout_conversion_rate=round((checkouts / add_to_carts) * 100, 2) if add_to_carts > 0 else 0,
            purchase_conversion_rate=round((orders / visitors) * 100, 2) if visitors > 0 else 0,
            traffic_sources=traffic_sources,
            device_breakdown=device_breakdown
        )
        
        db.session.add(metrics)
    
    db.session.commit()
    
    # Generate funnel stages for the last 30 days
    for i in range(30):
        date = (datetime.utcnow() - timedelta(days=29-i)).date()
        
        stages = [
            ('visit', 45000, 45000, 100.0),
            ('product_view', 45000, 22500, 50.0),
            ('add_to_cart', 22500, 6750, 30.0),
            ('checkout', 6750, 4050, 60.0),
            ('purchase', 4050, 2458, 60.7)
        ]
        
        for stage_name, visitors, conversions, rate in stages:
            funnel = FunnelStage(
                store_id=demo_store.id,
                date=date,
                stage_name=stage_name,
                visitors=visitors,
                conversions=conversions,
                dropoffs=visitors - conversions,
                conversion_rate=rate,
                industry_benchmark={
                    'visit': 100.0,
                    'product_view': 45.0,
                    'add_to_cart': 25.0,
                    'checkout': 55.0,
                    'purchase': 70.0
                }.get(stage_name, 0),
                percentile_rank=random.randint(35, 85)
            )
            db.session.add(funnel)
    
    db.session.commit()
    
    # Generate sample recommendations
    recommendations = [
        {
            'title': 'Fix checkout abandonment spike',
            'description': 'Your checkout abandonment increased 15% this week...',
            'category': 'conversion',
            'priority': 'critical',
            'impact_score': 92,
            'effort_score': 25,
            'potential_revenue': 8450,
            'generated_by': 'ai',
            'confidence': 0.89
        },
        {
            'title': 'Launch win-back email campaign',
            'description': 'You have 3,240 customers who haven\'t purchased in 90+ days...',
            'category': 'retention',
            'priority': 'high',
            'impact_score': 78,
            'effort_score': 35,
            'potential_revenue': 12400,
            'generated_by': 'ai',
            'confidence': 0.85
        },
        {
            'title': 'Optimize mobile product pages',
            'description': 'Mobile visitors convert 22% lower than desktop...',
            'category': 'conversion',
            'priority': 'high',
            'impact_score': 85,
            'effort_score': 45,
            'potential_revenue': 18600,
            'generated_by': 'ai',
            'confidence': 0.91
        }
    ]
    
    for rec_data in recommendations:
        rec = Recommendation(
            store_id=demo_store.id,
            **rec_data
        )
        db.session.add(rec)
    
    db.session.commit()
    
    print(f"✅ Generated sample data for UrbanThreads")
    print(f"   - 90 days of metrics")
    print(f"   - 30 days of funnel data")
    print(f"   - {len(recommendations)} recommendations")
