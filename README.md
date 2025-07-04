# 🤖 Linklet - Votre Assistant d'Automatisation Ultime

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-blue.svg)](https://docs.aiogram.dev/en/latest/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-blue.svg)](https://www.postgresql.org/)
[![n8n](https://img.shields.io/badge/n8n-Latest-orange.svg)](https://n8n.io/)
[![Redis](https://img.shields.io/badge/Redis-Latest-red.svg)](https://redis.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Latest-green.svg)](https://openai.com/)

Linklet est un bot Telegram nouvelle génération conçu pour être votre assistant ultime en matière d'automatisation, d'intégration d'APIs et de gestion intelligente de tâches. Son nom évoque sa capacité à faire le **lien (Link)** entre diverses plateformes tout en restant **léger (let)** et facile à utiliser.

## 📖 À Propos du Projet

Linklet a été créé pour répondre aux besoins croissants d'automatisation et d'intégration dans le monde numérique actuel. Il permet aux utilisateurs de :

- **Particuliers** : Automatiser leurs tâches quotidiennes, gérer leurs rappels, surveiller leurs données
- **Freelances/PME** : Optimiser leur workflow, automatiser leur facturation, suivre leur activité
- **Développeurs** : Étendre les fonctionnalités via une API flexible et des webhooks
- **Communautés** : Gérer la modération, organiser des événements, collecter des données

## 🌟 Fonctionnalités

- **Automatisation Puissante**
  - Déclenchement de workflows depuis Telegram
  - Synchronisation multi-outils (Google Sheets → Notion, Discord → Trello, etc.)
  - Templates d'automatisation partageables
  - Planification de tâches récurrentes
  - Webhooks personnalisables

- **Intelligence Artificielle**
  - Chat contextuel avec mémoire des conversations
  - Personnalisation du ton et du style
  - Génération de contenu (résumés, traductions, rédaction)
  - Analyse de données (fichiers CSV, extraits web)
  - Intégration avec GPT-4, Gemini et Mistral

- **Gestion des Tâches**
  - Création de tâches (ponctuelles ou récurrentes)
  - Alertes intelligentes (horaire, géolocalisation, événements externes)
  - Suivi de projets (Kanban intégré, rapports automatisés)
  - Rappels personnalisables
  - Gestion des priorités

- **Intégrations Universelles**
  - Connecteurs prêts à l'emploi (Airtable, Slack, GitHub, etc.)
  - API personnalisable pour les développeurs
  - Webhooks entrants/sortants
  - Support pour les services cloud populaires
  - Extensible via plugins

## 🛠 Stack Technique

- **Backend** : Python avec aiogram 3.x pour l'interface Telegram
- **Base de données** : PostgreSQL pour les données structurées, Redis pour le cache
- **Workflows** : n8n (auto-hébergé ou cloud) pour l'automatisation
- **IA** : OpenAI API (GPT-4), Google Gemini, Mistral (auto-hébergé)
- **Hébergement** : VPS (Hetzner, DigitalOcean) ou Serverless (AWS Lambda)
- **Monitoring** : Prometheus + Grafana pour la supervision
- **Tests** : pytest pour les tests unitaires et d'intégration

## 📋 Prérequis

- Python 3.12 ou supérieur
- PostgreSQL 15 ou supérieur
- Redis 7 ou supérieur
- n8n (optionnel pour les fonctionnalités d'automatisation)
- Un token de bot Telegram (via @BotFather)
- Accès aux APIs d'IA (clés API pour OpenAI, Google, etc.)

## 🚀 Démarrage Rapide

1. **Cloner le dépôt**
   ```powershell
   git clone https://github.com/yourusername/linklet.git
   cd linklet
   ```

2. **Créer et activer l'environnement virtuel**
   ```powershell
   python -m venv env
   .\env\Scripts\Activate.ps1
   ```

3. **Installer les dépendances**
   ```powershell
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Configurer l'environnement**
   ```powershell
   Copy-Item .env.example .env
   # Éditez le fichier .env avec vos configurations
   ```

5. **Initialiser la base de données**
   ```powershell
   alembic upgrade head
   ```

6. **Démarrer le bot**
   ```powershell
   python -m src.bot.main
   ```

## 🏗 Structure du Projet

```
linklet/
├── src/
│   ├── bot/           # Code du bot Telegram
│   │   ├── handlers/  # Gestionnaires de commandes
│   │   ├── middleware/# Middlewares (auth, rate limit)
│   │   └── utils/     # Utilitaires (keyboards, messages)
│   ├── core/          # Fonctionnalités principales
│   │   ├── database/  # Modèles et migrations
│   │   ├── services/  # Services métier
│   │   └── cache/     # Gestion du cache
│   ├── api/           # API REST
│   ├── workers/       # Tâches en arrière-plan
│   └── integrations/  # Services tiers
├── tests/             # Suite de tests
└── docs/             # Documentation
```

## 🔄 Workflow de Développement

1. **Préparation**
   - Créer une branche de fonctionnalité
   - Activer l'environnement virtuel
   - Installer les dépendances de développement

2. **Développement**
   - Écrire les tests
   - Implémenter les fonctionnalités
   - Suivre les conventions de code (black, isort)

3. **Tests**
   ```powershell
   # Lancer les tests
   pytest
   
   # Vérifier la couverture
   pytest --cov=src
   ```

4. **Validation**
   - Push vers la branche
   - Créer une pull request
   - Attendre la review

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🤝 Contribuer

Les contributions sont les bienvenues ! Consultez nos [Directives de Contribution](CONTRIBUTING.md) pour plus d'informations.

## 🔜 Roadmap

### Phase 1 (MVP) - En cours
- [x] Configuration du projet
- [x] Commandes de base du bot
- [x] Intégration n8n
- [ ] Documentation utilisateur
- [ ] Tests de base

### Phase 2 (AI & Connecteurs)
- [ ] Intégration IA (GPT-4, Gemini)
- [ ] Connecteurs Notion et Google
- [ ] Système de templates
- [ ] Tests d'intégration

### Phase 3 (Marketplace)
- [ ] Marketplace de templates
- [ ] Système de paiement
- [ ] Interface web admin
- [ ] Documentation API

---

Fait avec ❤️ par DataCraft Lab
