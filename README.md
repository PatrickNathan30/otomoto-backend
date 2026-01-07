# OTOMOTO – Backend (MVP)

## 1. Présentation générale

Ce dépôt contient le **backend du MVP OTOMOTO**, développé dans le cadre d’un **stage backend**.  
Le projet OTOMOTO est une plateforme de type **marketplace automobile multi-vendeurs**, dédiée à la gestion et à la vente de pièces détachées automobiles.

Le backend a été conçu pour fournir :
- une API REST modulaire et sécurisée,
- la gestion des stocks et des vendeurs,
- un système de traçabilité des pièces,
- un module de paiement interne (wallet / fintech).

## 2. Périmètre du backend

Le backend couvre exclusivement les fonctionnalités suivantes :

- Gestion des utilisateurs et des vendeurs
- Gestion des inventaires de pièces détachées
- Traçabilité des pièces (logique de chaînage par hash)
- Module de paiement interne (OtoPay)
- Exposition des fonctionnalités via une API REST

**Le frontend, la blockchain déployée, les tableaux de bord PowerBI et les environnements de production ne font pas partie de ce dépôt.**

## 3. Architecture technique

### 3.1 Technologies utilisées

- **Python**
- **Django**
- **Django REST Framework**
- **SQLite** (environnement de développement)
- **python-dotenv** pour la gestion des variables d’environnement

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
DJANGO_DEBUG=True ```


## 6. Installation et exécution locale

### 6.1 Prérequis

- Python 3.x  
- Environnement virtuel Python (venv)


### 6.2 Installation des dépendances

Installer les dépendances du projet à l’aide du fichier `requirements.txt` :

```bash
pip install -r requirements.txt


### 6.3 Migrations de la base de données

Appliquer les migrations Django afin de créer et mettre à jour le schéma de la base de données :

```bash
python manage.py migrate

### 6.4 Lancement du serveur de développement

Démarrer le serveur de développement Django :

```bash
python manage.py runserver


## 7. Tests

Les tests inclus dans le cadre de ce backend concernent principalement :

- la validation des modèles,
- les endpoints de l’API REST,
- les règles de permissions et de contrôle d’accès.

Les tests de performance, les audits de sécurité OWASP ainsi que les tests end-to-end globaux ne faisaient pas partie du périmètre direct du stage backend.



## 8. Contexte du projet

Ce backend a été développé dans un **contexte de MVP (Minimum Viable Product)**, avec pour objectifs principaux :

- appliquer les bonnes pratiques de développement avec Django REST Framework,
- concevoir une architecture modulaire, claire et maintenable,
- sécuriser les données sensibles et les paramètres de configuration,
- fournir une base technique solide pour les évolutions post-MVP.


## 9. Limites connues

Les limites actuelles du backend sont les suivantes :

- utilisation de **SQLite** comme base de données (environnement de développement),
- absence de déploiement en environnement de production,
- blockchain non déployée (logique préparatoire uniquement côté backend).


## 10. Auteur

**Patrick Nathan**  
Stagiaire Backend – Projet OTOMOTO

