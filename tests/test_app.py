"""
ShopifyPulse Tests
"""

import pytest
from app import app, db
from models.store import Store

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_landing_page(client):
    """Test landing page loads"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'ShopifyPulse' in response.data

def test_demo_page(client):
    """Test demo dashboard loads"""
    response = client.get('/demo')
    assert response.status_code == 200
    assert b'Dashboard' in response.data

def test_dashboard_metrics_api(client):
    """Test dashboard metrics API"""
    response = client.get('/api/v1/metrics/dashboard?store_id=demo&period=30d')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data

def test_funnel_data_api(client):
    """Test funnel data API"""
    response = client.get('/api/v1/metrics/funnel?store_id=demo&period=30d')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'stages' in data['data']

def test_recommendations_api(client):
    """Test recommendations API"""
    response = client.get('/api/v1/recommendations?store_id=demo&limit=5')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert len(data['data']) <= 5

def test_store_overview_api(client):
    """Test store overview API"""
    response = client.get('/api/v1/store/overview?store_id=demo')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['name'] == 'UrbanThreads'

def test_alerts_api(client):
    """Test alerts API"""
    response = client.get('/api/v1/alerts?store_id=demo')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
