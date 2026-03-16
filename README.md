# Pinterest Trending Pins Recommender

**Live Application:** https://pinterest-analytics.vercel.app/

A full-stack ML-powered recommendation engine that analyzes Pinterest user behavior and pin engagement to deliver personalized content recommendations in real-time. Built with collaborative filtering and matrix factorization for optimized content discovery.

---

## Overview

The Pinterest Trending Pins Recommender processes Pinterest-like social media data to surface relevant content faster. The system identifies emerging trends across categories like Fashion, Home Decor, Food, and Travel — compressing trend identification from weeks to hours.

**Key capabilities:**
- Personalized pin recommendations using collaborative filtering on user interaction history
- Real-time trending detection across 10+ content categories
- Comprehensive analytics dashboard with engagement metrics and system health monitoring

---

## Architecture

The system follows a microservices architecture with clear separation between the frontend, backend, ML pipeline, and streaming layers.

**Frontend (React + Vercel)**
- Interactive analytics dashboard built with Recharts
- Real-time metrics display and recommendation performance monitoring

**Backend (Django + PostgreSQL)**
- Django REST Framework API with Redis caching layer
- Celery background tasks for async ML model training

**ML Pipeline (Scikit-learn + AWS SageMaker)**
- Collaborative filtering and matrix factorization for user-based recommendations
- Content-based filtering using pin metadata and TF-IDF
- Hybrid approach combining multiple algorithms for improved accuracy

**Streaming (Apache Kafka)**
- Real-time user interaction event processing
- Live recommendation updates and analytics pipeline

**Data Flow:**
1. User interactions captured via Django API
2. Events streamed through Kafka for immediate processing
3. ML models generate personalized recommendations
4. Results cached in Redis for fast retrieval
5. Analytics dashboard displays live performance metrics

---

## Features

- **Real-time Recommendation Engine** — Collaborative filtering analyzes user behavior to surface relevant pins with sub-20ms response times via Redis caching
- **Trending Content Detection** — ML pipeline identifies viral pins and emerging trends across 10+ categories
- **Performance Analytics** — Dashboard tracks CTR, engagement rates, recommendation accuracy, and system health in real-time
- **Scalable Infrastructure** — Kafka streaming + SageMaker inference designed for high-throughput recommendation serving

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/recommendations/{user_id}/` | Personalized pin recommendations with confidence scores |
| `GET` | `/api/trending/` | Trending pins with optional category and time range filters |
| `POST` | `/api/interactions/` | Records user interactions and triggers real-time model updates |
| `GET` | `/api/analytics/dashboard/` | Dashboard KPIs, engagement trends, and system health |
| `GET` | `/api/users/{user_id}/profile/` | User profile with preference analysis and activity history |

---

## Data Pipeline

**Data Generation**
- Faker-generated Pinterest-like dataset: 50K+ pins, 2K+ users, 48K+ interactions across 10 categories

**Feature Engineering**
- User preference vectors from interaction history
- Pin popularity scores based on engagement signals
- Temporal features for trending detection
- Category embeddings for content similarity

**Model Training**
- Collaborative filtering with user-item matrices
- Matrix factorization with SGD optimization
- Hybrid approach combining collaborative + content-based signals

**Real-time Inference**
- Redis caching for high-frequency requests
- Kafka streaming for live recommendation updates
- AWS SageMaker for scalable model serving

---

## Project Structure

```
pinterest-analytics/
├── frontend/                 # React dashboard
├── apps/core/                # Django models
├── apps/recommendations/     # ML recommendation engine
├── apps/analytics/           # Dashboard APIs
├── src/models/               # ML algorithms
├── data/raw/                 # Generated datasets
├── ml_pipeline/              # Training scripts
└── scripts/                  # Utility scripts
```

---

## Tech Stack

`Django` `PostgreSQL` `Redis` `Apache Kafka` `React.js` `Scikit-learn` `AWS SageMaker` `Docker` `Vercel`