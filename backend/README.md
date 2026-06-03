# GBSB Digital Gurukul - Backend

FastAPI-based REST API for Digital Gurukul Platform

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: http://localhost:8000
API Docs: http://localhost:8000/docs

## Database Setup

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE gbsb_gurukul;

# Run migrations
alembic upgrade head
```
