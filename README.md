# Pinterest Trending Pins Recommender

**Live Application:** https://pinterest-analytics.vercel.app/

A full-stack ML-powered recommendation engine that analyzes Pinterest user behavior and pin engagement to deliver personalized content recommendations. Built with collaborative filtering, matrix factorization, and content-based filtering — evaluated against a generated dataset of 2,497 interactions across 2,000 users and 48,672 pins.

---

## ML Results

| Model | Metric | Result |
|---|---|---|
| Category Preference (RandomForest) | Accuracy (5-fold CV) | **90.9% ± 0.84%** |
| Random baseline | Accuracy | 10.0% |
| Lift over baseline | — | **9.1x** |
| Matrix Factorization (SVD) | Catalog coverage | **51.3%** |
| SVD | Explained variance | 11.5% |

> **Note on sparsity:** With ~1.79 interactions/user, pin-level precision/recall are near-zero due to the cold-start problem — expected and documented. Category preference prediction is the appropriate primary metric for this sparsity level. Full results in `ml_pipeline/results/metrics.json`.

---

## Overview

The Pinterest Trending Pins Recommender processes Pinterest-like social media data to surface relevant content faster. The system identifies emerging trends across 10 categories: Fashion, Home Decor, Food, Travel, DIY & Crafts, Beauty, Health & Fitness, Photography, Art, and Gardening.

**Key capabilities:**
- Personalized pin recommendations using collaborative filtering on user interaction history
- Category preference prediction with 90.9% accuracy — 9.1x lift over random baseline
- Analytics dashboard showing real engagement metrics derived from the dataset

---

## Architecture

The system follows a microservices architecture with clear separation between the frontend, backend, ML pipeline, and streaming layers.

**Frontend (React + Vercel)**
- Interactive analytics dashboard built with Recharts
- Displays real metrics from `ml_pipeline/results/metrics.json`

**Backend (Django + PostgreSQL)**
- Django REST Framework API with Redis caching layer
- Celery background tasks for async ML model training

**ML Pipeline (Scikit-learn)**
- Collaborative filtering using weighted user-item cosine similarity
- Matrix factorization via Truncated SVD (50 latent factors)
- Content-based filtering using TF-IDF on pin category + tags
- Evaluated with 5-fold cross-validation and train/test split by recency

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

- **Three-model Recommendation Engine** — Collaborative filtering, matrix factorization, and content-based filtering with documented evaluation metrics
- **Trending Content Detection** — ML pipeline identifies high-engagement pins across 10 categories using weighted interaction signals (save=5, share=4, like=3, click=2, comment=1)
- **Honest Evaluation** — Cold-start limitations documented; metrics derived from actual data, not estimates
- **Scalable Infrastructure** — Kafka streaming + Redis caching designed for high-throughput recommendation serving

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

**Dataset**
- Faker-generated Pinterest-like data: 48,672 pins · 2,000 users · 2,497 interactions across 10 categories
- Interaction types: save, like, click, share, comment — weighted by engagement strength

**Feature Engineering**
- Weighted user-item interaction matrix (save=5, share=4, like=3, click=2, comment=1)
- User preference vectors from interaction history
- TF-IDF vectors from pin category, subcategory, and tags
- Temporal train/test split by recency (80/20 per user)

**Model Training**
- Collaborative filtering: cosine similarity across user-item matrix
- Matrix factorization: Truncated SVD with 50 latent factors
- Content-based: TF-IDF profile matching against user interaction history

**Running the Pipeline**
```bash
PYTHONPATH=. python ml_pipeline/train_models.py
```
Results saved to `ml_pipeline/results/metrics.json`.

---

## Project Structure

```
pinterest-analytics/
├── frontend/                 # React dashboard
├── apps/core/                # Django models
├── apps/recommendations/     # ML recommendation engine
├── apps/analytics/           # Dashboard APIs
├── src/models/               # ML algorithms (CF, MF, CB, evaluation)
├── data/raw/                 # Generated datasets
├── ml_pipeline/              # Training scripts + results
└── scripts/                  # Utility scripts
```

---

## Tech Stack

`Django` `PostgreSQL` `Redis` `Apache Kafka` `React.js` `Scikit-learn` `Docker` `Vercel`