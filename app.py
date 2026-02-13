"""
ShopifyPulse - Main Flask Application
Agent 3.1 - E-commerce Dashboard for SMB Stores
"""

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///shopifypulse.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Import models and routes after app initialization
from models.store import Store, StoreMetrics, FunnelStage
from models.user import User
from api.analytics import get_dashboard_metrics, get_funnel_data
from api.recommendations import generate_recommendations

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============================================
# ROUTES
# ============================================

@app.route('/')
def index():
    """Landing page"""
    return render_template('landing.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/demo')
def demo():
    """Interactive demo with sample data"""
    return render_template('demo.html')

# ============================================
# API ENDPOINTS
# ============================================

@app.route('/api/v1/metrics/dashboard', methods=['GET'])
def api_dashboard_metrics():
    """Get dashboard metrics for a store"""
    store_id = request.args.get('store_id', 'demo')
    period = request.args.get('period', '30d')
    
    metrics = get_dashboard_metrics(store_id, period)
    return jsonify({
        'success': True,
        'data': metrics,
        'generated_at': datetime.utcnow().isoformat()
    })

@app.route('/api/v1/metrics/funnel', methods=['GET'])
def api_funnel_data():
    """Get funnel visualization data"""
    store_id = request.args.get('store_id', 'demo')
    period = request.args.get('period', '30d')
    
    funnel_data = get_funnel_data(store_id, period)
    return jsonify({
        'success': True,
        'data': funnel_data,
        'generated_at': datetime.utcnow().isoformat()
    })

@app.route('/api/v1/recommendations', methods=['GET'])
def api_recommendations():
    """Get AI-powered recommendations"""
    store_id = request.args.get('store_id', 'demo')
    limit = int(request.args.get('limit', 5))
    
    recommendations = generate_recommendations(store_id, limit)
    return jsonify({
        'success': True,
        'data': recommendations,
        'count': len(recommendations),
        'generated_at': datetime.utcnow().isoformat()
    })

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/v1/store/overview', methods=['GET'])
def api_store_overview():
    """Get store overview information"""
    store_id = request.args.get('store_id', 'demo')
    
    # Demo store data
    overview = {
        'id': store_id,
        'name': 'UrbanThreads',
        'platform': 'Shopify',
        'url': 'urbanthreads-demo.myshopify.com',
        'annual_revenue': 2300000,
        'monthly_visitors': 45000,
        'conversion_rate': 3.2,
        'aov': 78,
        'ltv': 156,
        'tier': 'Scale',
        'connected_at': '2024-01-15T10:30:00Z',
        'last_sync': datetime.utcnow().isoformat(),
        'health_score': 87
    }
    
    return jsonify({
        'success': True,
        'data': overview
    })

@app.route('/api/v1/alerts', methods=['GET'])
def api_alerts():
    """Get active alerts for a store"""
    store_id = request.args.get('store_id', 'demo')
    
    alerts = [
        {
            'id': 'alert_001',
            'type': 'warning',
            'title': 'Cart abandonment spike',
            'message': 'Cart abandonment increased 12% this week',
            'impact': 'high',
            'suggestion': 'Review shipping costs and checkout flow',
            'created_at': (datetime.utcnow() - timedelta(hours=2)).isoformat()
        },
        {
            'id': 'alert_002',
            'type': 'opportunity',
            'title': 'Email list growth opportunity',
            'message': 'Exit intent popup could capture 15% more emails',
            'impact': 'medium',
            'suggestion': 'Implement exit-intent popup with 10% discount',
            'potential_revenue': '$2,400/month',
            'created_at': (datetime.utcnow() - timedelta(days=1)).isoformat()
        }
    ]
    
    return jsonify({
        'success': True,
        'data': alerts,
        'count': len(alerts)
    })

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# ============================================
# CLI COMMANDS
# ============================================

@app.cli.command('init-db')
def init_db():
    """Initialize the database with demo data"""
    db.create_all()
    print('Database initialized!')
    
    # Create demo store
    demo_store = Store(
        name='UrbanThreads',
        platform='shopify',
        url='urbanthreads-demo.myshopify.com',
        annual_revenue=2300000,
        is_active=True
    )
    db.session.add(demo_store)
    db.session.commit()
    print('Demo store created!')

@app.cli.command('seed-data')
def seed_data():
    """Seed database with sample metrics data"""
    from utils.seed_data import generate_sample_data
    generate_sample_data()
    print('Sample data generated!')

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
