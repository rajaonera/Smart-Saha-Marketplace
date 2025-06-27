# Sprint 1 – Smart Saha Marketplace (Backend)
## Objectif principal
Mettre en place la base technique backend solide : modèles, auth, premiers endpoints API, et tests basiques.

## Tâches principales
1. Organisation du projet
 Créer les dossiers models, services, tests dans l’app Django marketplace (via PowerShell : mkdir models,services,tests)

 Configurer settings.py (ajouter apps, config CORS, JWT, base de données Supabase)

2. Modèles de données essentiels
 Modèle Producteur (informations de base, contact, localisation)

 Modèle Produit (nom, description, prix, quantité, lien producteur)

 Modèle Entreprise (infos de l’acheteur)

 Modèle Commande (produit, quantité, producteur, entreprise, statut)

 Modèle Evaluation (liens commande, notes, commentaires)

3. Authentification JWT Supabase
 Configurer djangorestframework-simplejwt avec settings pour Supabase

 Endpoints : inscription, connexion, rafraîchissement token

4. API basiques
 CRUD Producteur (list, retrieve, create, update, delete)

 CRUD Produit (idem)

 Endpoint Marketplace : liste produits avec filtres simples (ex : par producteur, prix)

 Endpoint Commande : création commande + consultation

5. Services métiers
 Implémenter service pour gérer la création de commande (vérification stock, notifications éventuelles)

6. Tests unitaires
 Tests modèles Producteur, Produit

 Tests services (création commande)

 Tests endpoints API CRUD Producteur et Produit

## Livrables Sprint 1
Code backend Django structuré en modules

Base de données avec tables clés créées

API fonctionnelles avec auth JWT

Tests automatisés pour les fonctions critiques

Documentation API minimale (Swagger ou drf-spectacular)

Durée estimée
2 à 3 semaines (selon disponibilité), avec revues hebdomadaires.

