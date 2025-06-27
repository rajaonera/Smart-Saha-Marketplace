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
