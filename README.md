# 🛒 Smart Saha – Module Marketplace

Bienvenue dans le module **Marketplace** de Smart Saha, une plateforme de mise en relation équitable entre **producteurs agricoles** et **entreprises privées**.

Ce module constitue une brique stratégique du projet, orientée **échange, négociation, traçabilité et transparence**.

---

## 🚀 Objectifs

- Publier des annonces de vente ou des appels d’offre
- Permettre des discussions privées entre utilisateurs
- Valider des transactions traçables
- Générer des logs justificatifs pour archivage ou litige
- Assurer une modération intelligente (IA + règles)
- Fournir des APIs propres pour le frontend et l’IA Agronomist

---

## 🧱 Stack technique

- **Backend** : Django 4.x (Python 3.10+)
- **API REST** : Django REST Framework
- **Base de données** : PostgreSQL (via Supabase)
- **Authentification** : Supabase Auth (JWT)
- **Modèle IA** : Deepseek R1 (Agronomist AI)

---

## 📦 Structure des entités principales

| Entité | Description |
|--------|-------------|
| `Utilisateur` | Acteurs de la plateforme (producteurs, entreprises, admins) |
| `Annonce` | Offre de vente ou appel d’offre |
| `Message` | Messagerie privée liée à une annonce |
| `Transaction` | Enregistrement d’un deal conclu |
| `LogEchange` | Historique d’échanges pour traçabilité |
| `AlerteModeration` | Système de détection automatique d’anomalies |
| `Produit` | Référentiel des produits agricoles |

---

## 📁 Structure du projet

```shell
marketplace/
├── models/
│   ├── annonce.py
│   ├── message.py
│   ├── transaction.py
│   ├── produit.py
│   └── logs.py
├── services/
│   ├── annonce_service.py
│   └── moderation_service.py
├── serializers.py
├── views.py
├── permissions.py
├── urls.py
└── tests/

```
# Installation (local)

```shell
# Cloner le repo
git clone https://github.com/ton-org/smart-saha-backend.git
cd smart-saha-backend

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
python manage.py runserver
```

⚠️ Configurer .env avec les clés Supabase, la connexion DB, et la secret key Django.

🔐 Authentification
Les utilisateurs s’authentifient via Supabase Auth.
Le backend Django valide les JWT et attribue dynamiquement le rôle (producteur, entreprise, admin).

🔌 Extrait des routes API
Méthode	Route	Description
GET	/api/annonces/	Lister les annonces
POST	/api/annonces/	Créer une annonce
GET	/api/messages/?annonce=ID	Voir les messages liés
POST	/api/messages/	Envoyer un message
POST	/api/transactions/	Valider un accord
GET	/api/logs/?annonce=ID	Voir les logs d’un échange

Feedback & réputation utilisateur

Génération automatique de contrats en PDF

Interface d’administration avancée pour les modérateurs

📜 Licence
Projet open-source sous licence MIT (à confirmer avec l'équipe).
