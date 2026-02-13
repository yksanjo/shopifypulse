"""
Shopify API Integration
Handles OAuth, data fetching, and webhook processing
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

SHOPIFY_API_VERSION = '2024-01'

class ShopifyClient:
    """Client for interacting with Shopify API"""
    
    def __init__(self, shop_domain: str, access_token: str):
        self.shop_domain = shop_domain
        self.access_token = access_token
        self.base_url = f"https://{shop_domain}/admin/api/{SHOPIFY_API_VERSION}"
        
    def _make_request(self, endpoint: str, method: str = 'GET', params: Dict = None, json_data: Dict = None) -> Dict:
        """Make authenticated request to Shopify API"""
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'X-Shopify-Access-Token': self.access_token,
            'Content-Type': 'application/json'
        }
        
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=json_data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    def get_shop_info(self) -> Dict:
        """Get shop information"""
        return self._make_request('shop.json')
    
    def get_orders(self, limit: int = 250, since_id: str = None, 
                   created_at_min: str = None, created_at_max: str = None) -> List[Dict]:
        """Get orders with optional filtering"""
        params = {'limit': limit}
        if since_id:
            params['since_id'] = since_id
        if created_at_min:
            params['created_at_min'] = created_at_min
        if created_at_max:
            params['created_at_max'] = created_at_max
            
        response = self._make_request('orders.json', params=params)
        return response.get('orders', [])
    
    def get_products(self, limit: int = 250) -> List[Dict]:
        """Get products"""
        response = self._make_request('products.json', params={'limit': limit})
        return response.get('products', [])
    
    def get_customers(self, limit: int = 250) -> List[Dict]:
        """Get customers"""
        response = self._make_request('customers.json', params={'limit': limit})
        return response.get('customers', [])
    
    def get_analytics(self, report_type: str, start_date: str, end_date: str) -> Dict:
        """Get analytics data using ShopifyQL or Reports API"""
        # This would use Shopify's Reports API for actual data
        # For now, returning mock structure
        return {
            'report_type': report_type,
            'start_date': start_date,
            'end_date': end_date,
            'data': []
        }
    
    def get_checkouts(self, limit: int = 250) -> List[Dict]:
        """Get abandoned checkouts"""
        response = self._make_request('checkouts.json', params={'limit': limit})
        return response.get('checkouts', [])


def get_oauth_url(shop_domain: str, redirect_uri: str, scopes: List[str] = None) -> str:
    """
    Generate OAuth URL for Shopify app installation
    
    Args:
        shop_domain: The shop's domain (e.g., 'store.myshopify.com')
        redirect_uri: The URL to redirect to after authorization
        scopes: List of permission scopes
    
    Returns:
        OAuth URL
    """
    if scopes is None:
        scopes = [
            'read_orders',
            'read_products',
            'read_customers',
            'read_analytics',
            'read_checkouts'
        ]
    
    api_key = os.getenv('SHOPIFY_API_KEY')
    scopes_str = ','.join(scopes)
    
    return (
        f"https://{shop_domain}/admin/oauth/authorize?"
        f"client_id={api_key}&"
        f"scope={scopes_str}&"
        f"redirect_uri={redirect_uri}"
    )


def exchange_code_for_token(shop_domain: str, code: str) -> str:
    """
    Exchange OAuth code for permanent access token
    
    Args:
        shop_domain: The shop's domain
        code: The authorization code from OAuth callback
    
    Returns:
        Access token
    """
    api_key = os.getenv('SHOPIFY_API_KEY')
    api_secret = os.getenv('SHOPIFY_API_SECRET')
    
    url = f"https://{shop_domain}/admin/oauth/access_token"
    payload = {
        'client_id': api_key,
        'client_secret': api_secret,
        'code': code
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    return response.json()['access_token']


def sync_store_data(store_id: int, client: ShopifyClient) -> Dict:
    """
    Sync store data from Shopify to local database
    
    Args:
        store_id: Local store ID
        client: Authenticated Shopify client
    
    Returns:
        Sync summary
    """
    # Get date range for sync
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    # Fetch data
    orders = client.get_orders(
        created_at_min=start_date.isoformat(),
        created_at_max=end_date.isoformat(),
        limit=250
    )
    
    checkouts = client.get_checkouts(limit=250)
    
    # Calculate metrics
    total_revenue = sum(float(order['total_price']) for order in orders)
    total_orders = len(orders)
    
    # Extract unique customers
    customer_ids = set(order['customer']['id'] for order in orders if order.get('customer'))
    
    return {
        'store_id': store_id,
        'sync_period': f"{start_date.date()} to {end_date.date()}",
        'orders_synced': total_orders,
        'revenue_synced': total_revenue,
        'customers_count': len(customer_ids),
        'abandoned_checkouts': len(checkouts),
        'synced_at': datetime.utcnow().isoformat()
    }


def verify_webhook(data: bytes, hmac_header: str, secret: str) -> bool:
    """
    Verify Shopify webhook HMAC signature
    
    Args:
        data: Raw request body
        hmac_header: X-Shopify-Hmac-SHA256 header value
        secret: Shopify API secret
    
    Returns:
        True if valid, False otherwise
    """
    import hmac
    import hashlib
    import base64
    
    digest = hmac.new(
        secret.encode('utf-8'),
        data,
        hashlib.sha256
    ).digest()
    
    computed_hmac = base64.b64encode(digest).decode('utf-8')
    return hmac.compare_digest(computed_hmac, hmac_header)
