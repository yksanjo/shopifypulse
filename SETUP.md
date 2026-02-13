# ShopifyPulse - Quick Setup Guide

## 🚀 5-Minute Quick Start

### Option 1: Local Development (Python)

```bash
# Navigate to project
cd shopifypulse

# Run startup script
./start.sh
```

The script will:
1. Create a virtual environment
2. Install dependencies
3. Set up the database
4. Generate sample data
5. Start the development server

Then open:
- **Landing Page:** http://localhost:5000
- **Demo Dashboard:** http://localhost:5000/demo

### Option 2: Docker (Recommended)

```bash
cd shopifypulse

# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d
```

Services:
- App: http://localhost:5000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Option 3: Heroku Deployment

```bash
# Install Heroku CLI, then:
heroku create your-shopifypulse-app
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
heroku config:set SHOPIFY_API_KEY=your_key
heroku config:set SHOPIFY_API_SECRET=your_secret

# Deploy
git push heroku main

# Run migrations
heroku run flask db upgrade
heroku run flask seed-data
```

---

## 📁 Project Structure

```
shopifypulse/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── SETUP.md               # This file
├── Dockerfile             # Docker image
├── docker-compose.yml     # Local stack
├── Procfile               # Heroku config
├── .env.example           # Environment template
├── start.sh               # Quick start script
│
├── api/                   # API modules
│   ├── analytics.py       # Dashboard metrics
│   ├── recommendations.py # AI recommendation engine
│   └── shopify.py         # Shopify integration
│
├── models/                # Database models
│   ├── store.py          # Store & metrics models
│   └── user.py           # User model
│
├── utils/                 # Utilities
│   └── seed_data.py      # Sample data generator
│
├── templates/             # HTML templates
│   ├── landing.html      # Marketing page
│   └── demo.html         # Dashboard
│
├── static/               # Frontend assets
│   ├── css/
│   │   └── dashboard.css
│   └── js/
│       └── dashboard.js
│
└── tests/                # Test suite
    └── test_app.py
```

---

## 🔌 API Endpoints

### Public Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Landing page |
| `GET /demo` | Interactive demo dashboard |
| `GET /api/v1/health` | Health check |

### Store Data Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/store/overview` | Store information |
| `GET /api/v1/metrics/dashboard` | Dashboard KPIs |
| `GET /api/v1/metrics/funnel` | Funnel visualization data |
| `GET /api/v1/recommendations` | AI recommendations |
| `GET /api/v1/alerts` | Active alerts |

### Example API Usage

```bash
# Get dashboard metrics
curl "http://localhost:5000/api/v1/metrics/dashboard?store_id=demo&period=30d"

# Get recommendations
curl "http://localhost:5000/api/v1/recommendations?store_id=demo&limit=5"

# Get funnel data
curl "http://localhost:5000/api/v1/metrics/funnel?store_id=demo&period=30d"
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_app.py::test_dashboard_metrics_api
```

---

## 🔧 Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Flask secret key |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `REDIS_URL` | No | Redis connection (for caching) |
| `SHOPIFY_API_KEY` | No | For Shopify integration |
| `SHOPIFY_API_SECRET` | No | For Shopify OAuth |
| `OPENAI_API_KEY` | No | For AI recommendations |

---

## 📦 Key Dependencies

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database
- **Plotly**: Interactive charts
- **Celery**: Background tasks
- **Redis**: Caching and task queue

---

## 🎯 Demo Data

The demo includes a fictional store:

**UrbanThreads** - Streetwear brand
- Annual Revenue: $2.3M
- Monthly Visitors: 45,000
- Conversion Rate: 5.46%
- AOV: $78
- LTV: $156

---

## 🚢 Production Deployment Checklist

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Use PostgreSQL (not SQLite)
- [ ] Enable SSL/TLS
- [ ] Set up monitoring (Sentry, New Relic)
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline
- [ ] Configure domain and DNS
- [ ] Set up email service (SendGrid/Mailgun)
- [ ] Configure Shopify app credentials
- [ ] Set up Stripe for billing

---

## 🆘 Troubleshooting

### Database errors
```bash
# Reset database
rm shopifypulse.db  # SQLite
flask init-db
flask seed-data
```

### Port already in use
```bash
# Use different port
flask run --port 5001
```

### Dependencies issues
```bash
# Clean install
rm -rf venv
./start.sh
```

---

## 📞 Support

- Documentation: See README.md
- Issues: Create a GitHub issue
- Email: support@shopifypulse.io

---

**Ready to launch your e-commerce analytics platform!** 🚀
