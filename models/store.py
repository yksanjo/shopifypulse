"""
Store and Metrics Models
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

class Store(db.Model):
    """E-commerce store entity"""
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # shopify, woocommerce
    url = db.Column(db.String(500))
    api_key = db.Column(db.String(500))
    api_secret = db.Column(db.String(500))
    access_token = db.Column(db.String(500))
    
    # Business metrics
    annual_revenue = db.Column(db.Numeric(12, 2))
    monthly_visitors = db.Column(db.Integer)
    conversion_rate = db.Column(db.Numeric(5, 2))
    aov = db.Column(db.Numeric(10, 2))  # Average Order Value
    ltv = db.Column(db.Numeric(10, 2))  # Lifetime Value
    
    # Subscription tier
    tier = db.Column(db.String(20), default='starter')  # starter, growth, scale
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_connected = db.Column(db.Boolean, default=False)
    connected_at = db.Column(db.DateTime)
    last_sync = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    metrics = db.relationship('StoreMetrics', backref='store', lazy=True)
    funnel_stages = db.relationship('FunnelStage', backref='store', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'platform': self.platform,
            'url': self.url,
            'annual_revenue': float(self.annual_revenue) if self.annual_revenue else None,
            'monthly_visitors': self.monthly_visitors,
            'conversion_rate': float(self.conversion_rate) if self.conversion_rate else None,
            'aov': float(self.aov) if self.aov else None,
            'ltv': float(self.ltv) if self.ltv else None,
            'tier': self.tier,
            'is_active': self.is_active,
            'is_connected': self.is_connected,
            'connected_at': self.connected_at.isoformat() if self.connected_at else None,
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'created_at': self.created_at.isoformat()
        }

class StoreMetrics(db.Model):
    """Time-series metrics for a store"""
    __tablename__ = 'store_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    # Traffic metrics
    sessions = db.Column(db.Integer, default=0)
    unique_visitors = db.Column(db.Integer, default=0)
    page_views = db.Column(db.Integer, default=0)
    bounce_rate = db.Column(db.Numeric(5, 2))
    avg_session_duration = db.Column(db.Integer)  # seconds
    
    # E-commerce metrics
    add_to_carts = db.Column(db.Integer, default=0)
    checkouts = db.Column(db.Integer, default=0)
    orders = db.Column(db.Integer, default=0)
    revenue = db.Column(db.Numeric(12, 2), default=0)
    
    # Calculated metrics
    cart_conversion_rate = db.Column(db.Numeric(5, 2))
    checkout_conversion_rate = db.Column(db.Numeric(5, 2))
    purchase_conversion_rate = db.Column(db.Numeric(5, 2))
    
    # Source breakdown (JSON for flexibility)
    traffic_sources = db.Column(db.JSON)
    device_breakdown = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'store_id': self.store_id,
            'date': self.date.isoformat(),
            'sessions': self.sessions,
            'unique_visitors': self.unique_visitors,
            'page_views': self.page_views,
            'bounce_rate': float(self.bounce_rate) if self.bounce_rate else None,
            'avg_session_duration': self.avg_session_duration,
            'add_to_carts': self.add_to_carts,
            'checkouts': self.checkouts,
            'orders': self.orders,
            'revenue': float(self.revenue) if self.revenue else 0,
            'cart_conversion_rate': float(self.cart_conversion_rate) if self.cart_conversion_rate else None,
            'checkout_conversion_rate': float(self.checkout_conversion_rate) if self.checkout_conversion_rate else None,
            'purchase_conversion_rate': float(self.purchase_conversion_rate) if self.purchase_conversion_rate else None,
            'traffic_sources': self.traffic_sources,
            'device_breakdown': self.device_breakdown
        }

class FunnelStage(db.Model):
    """Funnel stage performance data"""
    __tablename__ = 'funnel_stages'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    # Funnel stages
    stage_name = db.Column(db.String(50), nullable=False)  # visit, cart, checkout, purchase
    visitors = db.Column(db.Integer, default=0)
    conversions = db.Column(db.Integer, default=0)
    dropoffs = db.Column(db.Integer, default=0)
    conversion_rate = db.Column(db.Numeric(5, 2))
    
    # Benchmarks
    industry_benchmark = db.Column(db.Numeric(5, 2))
    percentile_rank = db.Column(db.Integer)  # 0-100
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'store_id': self.store_id,
            'date': self.date.isoformat(),
            'stage_name': self.stage_name,
            'visitors': self.visitors,
            'conversions': self.conversions,
            'dropoffs': self.dropoffs,
            'conversion_rate': float(self.conversion_rate) if self.conversion_rate else None,
            'industry_benchmark': float(self.industry_benchmark) if self.industry_benchmark else None,
            'percentile_rank': self.percentile_rank
        }

class Recommendation(db.Model):
    """AI-generated recommendations"""
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    
    # Recommendation details
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # conversion, retention, traffic, inventory
    priority = db.Column(db.String(20))  # critical, high, medium, low
    
    # Impact estimation
    impact_score = db.Column(db.Integer)  # 1-100
    effort_score = db.Column(db.Integer)  # 1-100 (1 = low effort)
    potential_revenue = db.Column(db.Numeric(10, 2))
    
    # Status
    is_implemented = db.Column(db.Boolean, default=False)
    implemented_at = db.Column(db.DateTime)
    dismissed = db.Column(db.Boolean, default=False)
    
    # Source
    generated_by = db.Column(db.String(50))  # ai, rule, manual
    confidence = db.Column(db.Numeric(4, 2))  # 0.00-1.00
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'store_id': self.store_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'impact_score': self.impact_score,
            'effort_score': self.effort_score,
            'potential_revenue': float(self.potential_revenue) if self.potential_revenue else None,
            'is_implemented': self.is_implemented,
            'confidence': float(self.confidence) if self.confidence else None,
            'created_at': self.created_at.isoformat()
        }
