# 🚀 Structure du Projet Linklet

## 📁 Architecture des Dossiers

```
linklet/
├── 📁 src/
│   ├── 📁 bot/
│   │   ├── __init__.py
│   │   ├── main.py                    # Point d'entrée du bot
│   │   ├── handlers/
│   │   │   ├── __init__.py
│   │   │   ├── basic.py               # Commandes de base
│   │   │   ├── automation.py          # Gestion workflows
│   │   │   ├── ai.py                  # Assistant IA
│   │   │   └── admin.py               # Commandes admin
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                # Authentification
│   │   │   ├── rate_limit.py          # Limitation de taux
│   │   │   └── logging.py             # Logs structurés
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── keyboards.py           # Claviers inline
│   │       └── messages.py            # Templates de messages
│   │
│   ├── 📁 core/
│   │   ├── __init__.py
│   │   ├── config.py                  # Configuration centralisée
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── models.py              # Modèles SQLAlchemy
│   │   │   ├── migrations/            # Migrations Alembic
│   │   │   └── connection.py          # Pool de connexions DB
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── workflow_service.py    # Logique métier workflows
│   │   │   ├── ai_service.py          # Intégration IA
│   │   │   ├── task_service.py        # Gestionnaire de tâches
│   │   │   └── integration_service.py # APIs externes
│   │   └── cache/
│   │       ├── __init__.py
│   │       └── redis_client.py        # Client Redis
│   │
│   ├── 📁 integrations/
│   │   ├── __init__.py
│   │   ├── base.py                    # Classe de base pour intégrations
│   │   ├── google/
│   │   │   ├── __init__.py
│   │   │   ├── drive.py
│   │   │   ├── sheets.py
│   │   │   └── calendar.py
│   │   ├── notion/
│   │   │   ├── __init__.py
│   │   │   └── client.py
│   │   ├── github/
│   │   │   ├── __init__.py
│   │   │   └── client.py
│   │   └── n8n/
│   │       ├── __init__.py
│   │       └── client.py
│   │
│   ├── 📁 workers/
│   │   ├── __init__.py
│   │   ├── celery_app.py              # Configuration Celery
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   ├── automation_tasks.py    # Tâches d'automatisation
│   │   │   ├── ai_tasks.py            # Tâches IA (async)
│   │   │   └── notification_tasks.py  # Notifications
│   │   └── scheduler.py               # Tâches récurrentes
│   │
│   └── 📁 api/
│       ├── __init__.py
│       ├── app.py                     # API REST (FastAPI)
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── webhooks.py            # Webhooks entrants
│       │   ├── integrations.py        # Gestion des intégrations
│       │   └── admin.py               # Interface admin
│       └── schemas/
│           ├── __init__.py
│           └── models.py              # Schémas Pydantic
│
├── 📁 tests/
│   ├── __init__.py
│   ├── conftest.py                    # Configuration pytest
│   ├── unit/
│   │   ├── test_handlers.py
│   │   ├── test_services.py
│   │   └── test_integrations.py
│   ├── integration/
│   │   ├── test_workflows.py
│   │   └── test_api.py
│   └── fixtures/
│       └── sample_data.py
│
├── 📁 deploy/
│   ├── docker/
│   │   ├── Dockerfile.bot
│   │   ├── Dockerfile.api
│   │   ├── docker-compose.yml
│   │   └── docker-compose.prod.yml
│   ├── k8s/                           # Kubernetes (optionnel)
│   │   ├── bot-deployment.yaml
│   │   ├── api-deployment.yaml
│   │   └── services.yaml
│   └── scripts/
│       ├── deploy.sh
│       ├── backup.sh
│       └── health_check.sh
│
├── 📁 docs/
│   ├── README.md
│   ├── CONTRIBUTING.md
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── user_guide/
│       ├── getting_started.md
│       ├── workflows.md
│       └── integrations.md
│
├── 📁 config/
│   ├── settings.py                    # Variables d'environnement
│   ├── logging.yaml                   # Configuration des logs
│   └── celery.conf
│
├── requirements.txt                   # Dépendances Python
├── requirements-dev.txt               # Dépendances développement
├── .env.example                       # Variables d'environnement exemple
├── .gitignore
├── Makefile                           # Commandes de développement
└── pyproject.toml                     # Configuration du projet
```

## 🔧 Technologies et Dépendances Principales

### Core Dependencies
```python
# Bot Framework
aiogram==3.1.1
aiohttp==3.8.6

# Database
sqlalchemy==2.0.21
alembic==1.12.0
psycopg2-binary==2.9.7
redis==5.0.0

# Task Queue
celery==5.3.1
flower==2.0.1

# API Framework
fastapi==0.103.1
uvicorn==0.23.2
pydantic==2.4.2

# AI Integration
openai==0.28.1
google-generativeai==0.1.0

# Integrations
google-api-python-client==2.98.0
notion-client==2.0.0
PyGithub==1.59.1
requests==2.31.0

# Monitoring & Logging
prometheus-client==0.17.1
structlog==23.1.0

# Testing
pytest==7.4.2
pytest-asyncio==0.21.1
pytest-cov==4.1.0
factory-boy==3.3.0
```

## ⚙️ Configuration Environnementale

### Variables d'Environnement (.env)
```env
# Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhook
TELEGRAM_WEBHOOK_SECRET=your_webhook_secret

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/linklet
REDIS_URL=redis://localhost:6379/0

# AI Services
OPENAI_API_KEY=your_openai_key
GOOGLE_AI_API_KEY=your_gemini_key

# Integrations
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
NOTION_TOKEN=your_notion_token
GITHUB_TOKEN=your_github_token

# n8n Integration
N8N_BASE_URL=https://your-n8n.com
N8N_API_KEY=your_n8n_api_key

# Security
JWT_SECRET_KEY=your_jwt_secret
ENCRYPTION_KEY=your_32_bytes_key

# Monitoring
SENTRY_DSN=your_sentry_dsn
LOG_LEVEL=INFO

# Performance
WORKER_CONCURRENCY=4
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW=60
```

## 📊 Modèles de Base de Données

### Structure des Tables Principales
```sql
-- Utilisateurs
users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    subscription_tier VARCHAR(50) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Workflows
workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    n8n_workflow_id VARCHAR(255),
    triggers JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tâches
tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    scheduled_at TIMESTAMP,
    completed_at TIMESTAMP,
    recurrence_rule VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Intégrations
integrations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    service_name VARCHAR(100) NOT NULL,
    credentials JSONB, -- Chiffré
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🚀 Plan de Développement en 4 Phases

### Phase 1: Foundation (Semaines 1-2)
- ✅ Setup projet et architecture
- ✅ Bot de base avec commandes essentielles
- ✅ Base de données et migrations
- ✅ Tests unitaires de base

### Phase 2: Core Features (Semaines 3-4)
- ✅ Intégration n8n basique
- ✅ Système de tâches et rappels
- ✅ 3 intégrations principales (Google, Notion, GitHub)
- ✅ Interface admin basique

### Phase 3: Advanced Features (Semaines 5-6)
- ✅ Assistant IA conversationnel
- ✅ Workflows complexes
- ✅ API REST complète
- ✅ Système de templates

### Phase 4: Production Ready (Semaines 7-8)
- ✅ Monitoring et métriques
- ✅ Déploiement automatisé
- ✅ Documentation utilisateur
- ✅ Tests de charge

## 🎯 Prochaines Étapes Immédiates

1. **Initialiser le projet** avec cette structure
2. **Configurer l'environnement de développement**
3. **Créer le bot de base** avec les commandes essentielles
4. **Setup de la base de données** avec les migrations
5. **Première intégration** avec n8n

Êtes-vous prêt à commencer ? Je peux vous guider pour chaque étape !