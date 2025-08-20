
#  Liste des API REST : backend Marketplace

### 1. **Inscription utilisateur**

* **URL:** `/api/register/`
* **Méthode:** POST
* **Description:** Permet à un nouvel utilisateur de s’inscrire en fournissant son username, email, catégorie utilisateur, et mot de passe.
* **Commentaires:**

  * Le mot de passe est hashé et stocké dans une table séparée `Password` pour la sécurité.
  * La catégorie utilisateur (ex: individuel, groupe, ONG) est obligatoire.

---

### 2. **Gestion des utilisateurs (CRUD)**

* **URL:** `/api/users/`
* **Méthodes:** GET, POST, PUT, PATCH, DELETE
* **Description:** Gestion complète des utilisateurs (lecture, création, modification, suppression).
* **Commentaires:**

  * Protégé par authentification (JWT).
  * Les infos sensibles (ex: mot de passe) ne sont pas exposées via l’API.

---

### 3. **Gestion des produits (CRUD)**

* **URL:** `/api/products/`
* **Méthodes:** GET, POST, PUT, PATCH, DELETE
* **Description:** Catalogue des produits avec leur unité de mesure.
* **Commentaires:**

  * Chaque produit est lié à une unité (ex: kg, litre).
  * La gestion de détails additionnels (description, qualité, etc.) peut se faire via un endpoint dédié (option nested serializer).

---

### 4. **Gestion des publications (annonces)**

* **URL:** `/api/posts/`
* **Méthodes:** GET, POST, PUT, PATCH, DELETE
* **Description:** Permet aux utilisateurs de créer, modifier, lister, supprimer des annonces de produits.
* **Commentaires:**

  * Inclut quantité, prix, localisation, catégorie, devise, image.
  * Lié aux tables `type_post`, `categorie_post`, `currency` pour classification.

---

### 5. **Gestion des conversations (chats)**

* **URL:** `/api/chats/`
* **Méthodes:** GET, POST, PUT, PATCH, DELETE
* **Description:** Gère les conversations liées aux publications entre utilisateurs.
* **Commentaires:**

  * Chaque chat est lié à une annonce (`post`).
  * Le statut de la conversation est géré (ex: en cours, terminée).

---

### 6. **Gestion des messages**

* **URL:** `/api/messages/`
* **Méthodes:** GET, POST, PUT, PATCH, DELETE
* **Description:** Permet l’échange de messages dans une conversation.
* **Commentaires:**

  * Messages liés à un utilisateur, un chat et un type de message (texte, image, etc.).

---

### 7. **Gestion des avis**

* **URL:** `/api/reviews/`
* **Méthodes:** GET, POST, PUT, PATCH, DELETE
* **Description:** Système d’évaluation entre utilisateurs avec notes et commentaires.
* **Commentaires:**

  * Permet un feedback entre vendeurs et acheteurs.

---

### 8. **Gestion des favoris**

* **URL:** `/api/favorites/`
* **Méthodes:** GET, POST, DELETE
* **Description:** Permet aux utilisateurs de sauvegarder leurs annonces préférées.
* **Commentaires:**

  * Relation unique par utilisateur/post.

---

### 9. **Gestion des signalements**

* **URL:** `/api/reports/`
* **Méthodes:** GET, POST, PUT, PATCH, DELETE
* **Description:** Signalement de contenus inappropriés (posts ou messages).
* **Commentaires:**

  * Soit sur un post, soit sur un message.
  * Statut du signalement (ex: en attente).

---

### 10. **Gestion des notifications**

* **URL:** `/api/notifications/`
* **Méthodes:** GET, POST, PUT, PATCH, DELETE
* **Description:** Notifications envoyées aux utilisateurs pour différents événements.
* **Commentaires:**

  * Statut lu/non lu.
  * Type de notification et référence possible à une ressource.

---

### 11. **Authentification JWT**

* **URLs:**

  * `/api/token/` (obtenir token)
  * `/api/token/refresh/` (rafraîchir token)
* **Méthode:** POST
* **Description:** Gère l’authentification sécurisée via JSON Web Token.

---

#  Notes supplémentaires

* Chaque API est **protégée par JWT** sauf l’inscription (`/api/register/`) qui est publique.

---