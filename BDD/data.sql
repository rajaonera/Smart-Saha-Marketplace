-- Données de test pour Smart Saha Marketplace

-- Catégories utilisateurs
INSERT INTO "categorie_user" (categorie) VALUES ('vendeur');
INSERT INTO "categorie_user" (categorie) VALUES ('acheteur');
INSERT INTO "categorie_user" (categorie) VALUES ('admin');

-- Utilisateurs
INSERT INTO "user" (username, email, justificatif_url) VALUES ('alice', 'alice@example.com', 'https://smart-saha.com/docs/alice.pdf');
INSERT INTO "user" (username, email, justificatif_url) VALUES ('bob', 'bob@example.com', 'https://smart-saha.com/docs/bob.pdf');
INSERT INTO "user" (username, email, justificatif_url) VALUES ('admin', 'admin@smart-saha.com', NULL);

-- Mots de passe
INSERT INTO "password" (id_user, password) VALUES (1, 'hashed_pwd1');
INSERT INTO "password" (id_user, password) VALUES (2, 'hashed_pwd2');
INSERT INTO "password" (id_user, password) VALUES (3, 'hashed_pwd3');

-- Types de publications
INSERT INTO "type_post" (type) VALUES ('offre');
INSERT INTO "type_post" (type) VALUES ('demande');

-- Catégories de publications
INSERT INTO "categorie_post" (categorie) VALUES ('fruits');
INSERT INTO "categorie_post" (categorie) VALUES ('légumes');

-- Devises
INSERT INTO "currency" (currency, iso_code) VALUES ('Ariary', 'MGA');
INSERT INTO "currency" (currency, iso_code) VALUES ('Euro', 'EUR');

-- Unités
INSERT INTO "unit" (unit) VALUES ('kg');
INSERT INTO "unit" (unit) VALUES ('litre');

-- Produits
INSERT INTO "product" (product, id_unit) VALUES ('banane', 1);
INSERT INTO "product" (product, id_unit) VALUES ('tomate', 1);

-- Publications
INSERT INTO "post" (
    id_type_post, description, id_user, quantity, price,
    location, image_url, id_categorie_post, id_currency, id_product
) VALUES (
    1, 'Vente de bananes bien mûres', 1, 100, 5000,
    'Toamasina', 'https://img.com/banane.jpg', 1, 1, 1
);

INSERT INTO "post" (
    id_type_post, description, id_user, quantity, price,
    location, image_url, id_categorie_post, id_currency, id_product
) VALUES (
    2, 'Recherche tomates fraîches', 2, 50, 7000,
    'Antananarivo', 'https://img.com/tomate.jpg', 2, 2, 2
);


-- Statuts
INSERT INTO "status" (status, expiration) VALUES ('en cours', 7);
INSERT INTO "status" (status, expiration) VALUES ('terminé', 0);

-- Chats
INSERT INTO "chat" (id_post, id_status) VALUES (1, 1);
INSERT INTO "chat" (id_post, id_status) VALUES (2, 1);

-- Types de message
INSERT INTO "type_message" (type) VALUES ('texte');
INSERT INTO "type_message" (type) VALUES ('image');

-- Messages
INSERT INTO "message" (message, id_user, id_chat, id_type_message)
VALUES ('Bonjour, votre offre m''intéresse', 2, 1, 1);
INSERT INTO "message" (message, id_user, id_chat, id_type_message)
VALUES ('Voici une photo', 1, 2, 2);

-- Types de PDF
INSERT INTO "type_pdf" (type) VALUES ('facture');
INSERT INTO "type_pdf" (type) VALUES ('contrat');

-- Documents PDF
INSERT INTO "pdf" (pdf, id_post, id_user, id_type_pdf) VALUES ('facture1.pdf', 1, 1, 1);
INSERT INTO "pdf" (pdf, id_post, id_user, id_type_pdf) VALUES ('contrat2.pdf', 2, 2, 2);

-- Avis
INSERT INTO "review" (id_user_from, id_user_to, rating, comment)
VALUES (2, 1, 5, 'Très bon vendeur');
INSERT INTO "review" (id_user_from, id_user_to, rating, comment)
VALUES (1, 2, 4, 'Acheteur sérieux');

-- Favoris
INSERT INTO "favorite" (id_user, id_post) VALUES (1, 2);
INSERT INTO "favorite" (id_user, id_post) VALUES (2, 1);

-- Signalements
INSERT INTO "report" (id_user, id_post, id_message, reason)
VALUES (1, 2, NULL, 'Contenu trompeur');
INSERT INTO "report" (id_user, id_post, id_message, reason)
VALUES (2, NULL, 2, 'Message inapproprié');

-- Tags
INSERT INTO "tag" (name) VALUES ('bio');
INSERT INTO "tag" (name) VALUES ('local');

-- Association post-tag
INSERT INTO "post_tag" (id_post, id_tag) VALUES (1, 1);
INSERT INTO "post_tag" (id_post, id_tag) VALUES (2, 2);

-- Notifications
INSERT INTO "notification" (id_user, message, notification_type, reference_id)
VALUES (1, 'Votre publication a été aimée', 'favori', 2);
INSERT INTO "notification" (id_user, message, notification_type, reference_id)
VALUES (2, 'Nouveau message reçu', 'message', 1);


-- Table des unités agricoles locales

INSERT INTO unit (unit, created_at)
VALUES ('Kapoka', '2025-07-02 10:00:00');

INSERT INTO unit (unit, created_at)
VALUES ('Vata', '2025-07-02 10:01:00');

INSERT INTO unit (unit, created_at)
VALUES ('Farantsa', '2025-07-02 10:02:00');

INSERT INTO unit (unit, created_at)
VALUES ('Gony (sac)', '2025-07-02 10:03:00');

INSERT INTO unit (unit, created_at)
VALUES ('Kilogramme', '2025-07-02 10:04:00');

INSERT INTO unit (unit, created_at)
VALUES ('Tonne', '2025-07-02 10:05:00');

INSERT INTO unit (unit, created_at)
VALUES ('Litres', '2025-07-02 10:06:00');

INSERT INTO unit (unit, created_at)
VALUES ('Bouteille (1L)', '2025-07-02 10:07:00');

INSERT INTO unit (unit, created_at)
VALUES ('Poche (légumes)', '2025-07-02 10:08:00');
-- Ariary malgache
INSERT INTO marketplace_currency (currency, iso_code, created_at)
VALUES ('Ariary', 'MGA', '2025-07-02 09:00:00');

-- Franc CFA
INSERT INTO marketplace_currency (currency, iso_code, created_at)
VALUES ('Franc CFA', 'XOF', '2025-07-02 09:01:00');

-- Dollar américain
INSERT INTO marketplace_currency (currency, iso_code, created_at)
VALUES ('Dollar américain', 'USD', '2025-07-02 09:02:00');

-- Euro
INSERT INTO marketplace_currency (currency, iso_code, created_at)
VALUES ('Euro', 'EUR', '2025-07-02 09:03:00');

-- Livre sterling
INSERT INTO marketplace_currency (currency, iso_code, created_at)
VALUES ('Livre sterling', 'GBP', '2025-07-02 09:04:00');

-- Yuan chinois
INSERT INTO marketplace_currency (currency, iso_code, created_at)
VALUES ('Yuan', 'CNY', '2025-07-02 09:05:00');
-- Table des unités agricoles locales
INSERT INTO marketplace_label (name) VALUES
('Bio'),
('Sans pesticide'),
('Agriculture durable'),
('Certification locale'),
('Produit frais'),
('Origine locale'),
('Sans OGM'),
('Commerce équitable'),
('Récolte récente'),
('Haute qualité'),
('Label rouge'),
('Produit de saison'),
('Respect de l’environnement');
