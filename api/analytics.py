"""
Analytics API - Dashboard metrics and funnel calculations
"""

from datetime import datetime, timedelta
import random
from typing import Dict, List, Any

def get_dashboard_metrics(store_id: str, period: str = '30d') -> Dict[str, Any]:
    """
    Get comprehensive dashboard metrics for a store
    
    Args:
        store_id: Store identifier
        period: Time period (7d, 30d, 90d, 1y)
    
    Returns:
        Dictionary containing all dashboard metrics
    """
    # Parse period
    days = {
        '7d': 7,
        '30d': 30,
        '90d': 90,
        '1y': 365
    }.get(period, 30)
    
    # Generate demo data for "UrbanThreads" store
    metrics = {
        'store_id': store_id,
        'period': period,
        'summary': {
            'total_revenue': 191667,
            'revenue_change': 12.5,
            'total_orders': 2458,
            'orders_change': 8.3,
            'total_visitors': 45000,
            'visitors_change': -2.1,
            'conversion_rate': 5.46,
            'conversion_change': 0.4,
            'aov': 78.00,
            'aov_change': 3.2,
            'ltv': 156.00,
            'ltv_change': 5.1
        },
        'revenue_trend': generate_revenue_trend(days),
        'traffic_sources': {
            'organic': {'visitors': 15750, 'percentage': 35, 'conversion': 4.2},
            'paid': {'visitors': 11250, 'percentage': 25, 'conversion': 6.8},
            'social': {'visitors': 9000, 'percentage': 20, 'conversion': 3.5},
            'email': {'visitors': 6750, 'percentage': 15, 'conversion': 8.2},
            'direct': {'visitors': 2250, 'percentage': 5, 'conversion': 5.1}
        },
        'device_breakdown': {
            'desktop': {'visitors': 18000, 'percentage': 40, 'conversion': 6.2},
            'mobile': {'visitors': 22500, 'percentage': 50, 'conversion': 4.8},
            'tablet': {'visitors': 4500, 'percentage': 10, 'conversion': 5.5}
        },
        'top_products': [
            {'name': 'Vintage Denim Jacket', 'revenue': 28500, 'units': 300, 'conversion': 7.2},
            {'name': 'Streetwear Hoodie', 'revenue': 22400, 'units': 280, 'conversion': 6.5},
            {'name': 'Graphic Tee Bundle', 'revenue': 18900, 'units': 450, 'conversion': 8.1},
            {'name': 'Canvas Sneakers', 'revenue': 15600, 'units': 195, 'conversion': 5.8},
            {'name': 'Urban Backpack', 'revenue': 12300, 'units': 123, 'conversion': 6.9}
        ],
        'cohort_analysis': generate_cohort_data(),
        'benchmarks': {
            'conversion_rate': {'store': 5.46, 'industry': 3.2, 'percentile': 85},
            'aov': {'store': 78, 'industry': 65, 'percentile': 72},
            'ltv_cac_ratio': {'store': 3.2, 'industry': 2.5, 'percentile': 78}
        }
    }
    
    return metrics

def get_funnel_data(store_id: str, period: str = '30d') -> Dict[str, Any]:
    """
    Get funnel visualization data with stage-by-stage analysis
    
    Args:
        store_id: Store identifier
        period: Time period
    
    Returns:
        Funnel data with conversion rates and benchmarks
    """
    # Demo funnel data
    funnel_data = {
        'store_id': store_id,
        'period': period,
        'stages': [
            {
                'name': 'Visit',
                'visitors': 45000,
                'conversions': 45000,
                'conversion_rate': 100.0,
                'dropoff_rate': 0.0,
                'industry_benchmark': 100.0,
                'percentile': 50,
                'value': 0,
                'status': 'normal'
            },
            {
                'name': 'Product View',
                'visitors': 45000,
                'conversions': 22500,
                'conversion_rate': 50.0,
                'dropoff_rate': 50.0,
                'industry_benchmark': 45.0,
                'percentile': 65,
                'value': 0,
                'status': 'good',
                'insight': 'Above average - product pages are engaging'
            },
            {
                'name': 'Add to Cart',
                'visitors': 22500,
                'conversions': 6750,
                'conversion_rate': 30.0,
                'dropoff_rate': 70.0,
                'industry_benchmark': 25.0,
                'percentile': 72,
                'value': 526500,
                'status': 'good',
                'insight': 'Strong ATC rate - pricing is competitive'
            },
            {
                'name': 'Checkout Started',
                'visitors': 6750,
                'conversions': 4050,
                'conversion_rate': 60.0,
                'dropoff_rate': 40.0,
                'industry_benchmark': 55.0,
                'percentile': 58,
                'value': 315900,
                'status': 'warning',
                'insight': 'Checkout abandonment higher than optimal'
            },
            {
                'name': 'Purchase Complete',
                'visitors': 4050,
                'conversions': 2458,
                'conversion_rate': 60.7,
                'dropoff_rate': 39.3,
                'industry_benchmark': 70.0,
                'percentile': 35,
                'value': 191716,
                'status': 'critical',
                'insight': 'Payment failures or unexpected costs'
            }
        ],
        'overall': {
            'visit_to_purchase_rate': 5.46,
            'industry_average': 3.2,
            'revenue_at_risk': 124184,
            'potential_recovery': 74400
        },
        'trends': {
            '7d': [5.1, 5.3, 5.2, 5.4, 5.5, 5.6, 5.46],
            '30d': generate_conversion_trend(30)
        }
    }
    
    return funnel_data

def generate_revenue_trend(days: int) -> List[Dict]:
    """Generate daily revenue trend data"""
    base_revenue = 6000
    trend = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i-1)
        # Add some randomness and weekly seasonality
        day_of_week = date.weekday()
        weekend_boost = 1.3 if day_of_week >= 5 else 1.0
        random_factor = random.uniform(0.85, 1.15)
        growth_factor = 1 + (i * 0.002)  # Slight upward trend
        
        revenue = round(base_revenue * weekend_boost * random_factor * growth_factor, 2)
        orders = int(revenue / 78)
        
        trend.append({
            'date': date.strftime('%Y-%m-%d'),
            'revenue': revenue,
            'orders': orders,
            'visitors': int(orders / 0.0546)
        })
    
    return trend

def generate_cohort_data() -> Dict:
    """Generate customer cohort retention data"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    cohorts = []
    
    for i, month in enumerate(months):
        customers = 400 + (i * 50)
        retention = [100]
        
        # Decaying retention rates
        for j in range(5 - i):
            retention.append(round(retention[-1] * random.uniform(0.35, 0.55), 1))
        
        cohorts.append({
            'month': month,
            'customers': customers,
            'retention': retention
        })
    
    return {
        'months': months,
        'cohorts': cohorts,
        'average_ltv': 156,
        'average_retention_3m': 28.5
    }

def generate_conversion_trend(days: int) -> List[float]:
    """Generate conversion rate trend over time"""
    base_rate = 5.0
    trend = []
    
    for i in range(days):
        # Random walk with slight upward trend
        change = random.uniform(-0.15, 0.20)
        base_rate = max(4.0, min(6.5, base_rate + change))
        trend.append(round(base_rate, 2))
    
    return trend

def calculate_health_score(metrics: Dict) -> int:
    """
    Calculate overall store health score (0-100)
    
    Based on:
    - Conversion rate vs benchmark (30%)
    - Revenue growth trend (25%)
    - Customer retention (20%)
    - Site performance (15%)
    - Inventory health (10%)
    """
    # Simplified calculation for demo
    score = 87
    return score
