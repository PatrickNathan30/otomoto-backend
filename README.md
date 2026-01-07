# OTOMOTO – Backend (MVP)

## 1. Présentation générale

Ce dépôt contient le **backend du MVP OTOMOTO**, développé dans le cadre d’un **stage backend**.  
Le projet OTOMOTO est une plateforme de type **marketplace automobile multi-vendeurs**, dédiée à la gestion et à la vente de pièces détachées automobiles.

Le backend a été conçu pour fournir :
- une API REST modulaire et sécurisée,
- la gestion des stocks et des vendeurs,
- un système de traçabilité des pièces,
- un module de paiement interne (wallet / fintech).

---

## 2. Périmètre du backend

Le backend couvre exclusivement les fonctionnalités suivantes :

- Gestion des utilisateurs et des vendeurs
- Gestion des inventaires de pièces détachées
- Traçabilité des pièces (logique de chaînage par hash)
- Module de paiement interne (OtoPay)
- Exposition des fonctionnalités via une API REST

⚠️ **Le frontend, la blockchain déployée, les tableaux de bord PowerBI et les environnements de production ne font pas partie de ce dépôt.**

---

## 3. Architecture technique

### 3.1 Technologies utilisées

- **Python**
- **Django**
- **Django REST Framework**
- **SQLite** (environnement de développement)
- **python-dotenv** pour la gestion des variables d’environnement

---

### 3.2 Structure du projet

otomoto_backend/
├── inventory/ # Gestion des pièces et inventaires
├── payments/ # Module fintech / wallet (OtoPay)
├── otomoto/ # Configuration globale Django
│ ├── settings.py
│ ├── urls.py
│ ├── asgi.py
│ └── wsgi.py
├── manage.py
├── requirements.txt
├── seed.py # Script d’initialisation de données
├── inventory_models.png


## 4. Description des modules

### 4.1 Module Inventory

Le module `inventory` gère :
- les pièces détachées,
- leur qualité,
- leur type de vendeur,
- leur disponibilité.

Il inclut :
- modèles (`models.py`)
- serializers (`serializers.py`)
- permissions (`permissions.py`)
- vues API (`views.py`)
- migrations versionnées

---

### 4.2 Traçabilité des pièces

Une logique de **traçabilité par chaînage de hash** a été implémentée afin de :
- garantir l’intégrité des données,
- détecter toute modification non autorisée,
- assurer un historique cohérent des pièces.

Cette logique constitue une **base backend compatible avec une future intégration blockchain**.


### 4.3 Module Payments (OtoPay)

Le module `payments` implémente :
- un wallet interne par utilisateur,
- l’historique des transactions,
- la gestion des crédits et débits,
- la base logique pour les remboursements.


## 5. Configuration et sécurité

### 5.1 Variables d’environnement

Les paramètres sensibles sont gérés via des variables d’environnement.

Un fichier d’exemple est fourni :

Exemple :
```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True

6. Installation et exécution locale
6.1 Prérequis
  Python 3.x
  Virtual environment (venv)

6.2 Installation
  pip install -r requirements.txt

6.3 Migrations
  python manage.py migrate

6.4 Lancement du serveur
  python manage.py runserver
  Le backend est accessible à l’adresse: http://127.0.0.1:8000/

7. Tests
Les tests inclus concernent principalement :

  la validation des modèles,
  
  les endpoints API,
  
  les règles de permissions.

Les tests de performance, OWASP et end-to-end globaux ne font pas partie du périmètre direct du stage backend.


8. Contexte du projet
Ce backend a été développé dans un contexte de MVP, avec pour objectifs :

  appliquer les bonnes pratiques Django REST,
  
  concevoir une architecture modulaire et maintenable,
  
  sécuriser les données sensibles,
  
  fournir une base solide pour les évolutions post-MVP.

9. Limites connues
  Base de données SQLite (usage développement)
  
  Pas de déploiement production inclus
  
  Blockchain non déployée (logique préparatoire uniquement)

Auteur
Patrick Nathan
Stagiaire Backend – Projet OTOMOTO
