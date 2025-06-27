-- Base de données Marketplace --

-- \c marketplace;

-- Table des catégories d'utilisateurs (ex: vendeur, acheteur, admin...)
-- Stocke les différents types d'utilisateurs possibles dans le système
CREATE TABLE "categorie_user"
(
    id               SERIAL PRIMARY KEY,
    categorie         VARCHAR(50)  NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des utilisateurs
-- Contient les informations de base des utilisateurs
CREATE TABLE "user"
(
    id               SERIAL PRIMARY KEY,
    username         VARCHAR(50)  NOT NULL,
    id_categorie_user INTEGER      NOT NULL,
    email            VARCHAR(100) NOT NULL UNIQUE,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    justificatif_url VARCHAR(255),
    foreign key (id_categorie_user) references categorie_user(id)
);

-- Table des mots de passe
-- Stocke les mots de passe des utilisateurs séparément pour plus de sécurité
CREATE TABLE "password"
(
    id               SERIAL PRIMARY KEY,
    id_user          INTEGER      NOT NULL,
    password         VARCHAR(255) NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des types de publications
-- Définit les différents types de posts possibles (ex: offre, demande...)
CREATE TABLE "type_post"
(
    id               SERIAL PRIMARY KEY,
    type             VARCHAR(50)  NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des catégories de publications
-- Permet de classer les publications par catégorie
CREATE TABLE "categorie_post"
(
    id               SERIAL PRIMARY KEY,
    categorie        VARCHAR(50)  NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des devises
-- Gère les différentes monnaies utilisées
create table "currency"(
    id               SERIAL PRIMARY KEY,
    currency         VARCHAR(50)  NOT NULL,
    iso_code         VARCHAR(50)  NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des unités de mesure
-- Stocke les différentes unités de mesure pour les produits
create table "unit"(
    id               SERIAL PRIMARY KEY,
    unit             VARCHAR(50)  NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des produits
-- Contient les informations sur les produits
create table "product"(
    id               SERIAL PRIMARY KEY,
    product          VARCHAR(50)  NOT NULL,
    id_unit          INTEGER      NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des publications
-- Stocke toutes les annonces/posts des utilisateurs
CREATE TABLE "post"
(
    id               SERIAL PRIMARY KEY,
    id_type_post     INTEGER      NOT NULL,
    id_product       INTEGER      NOT NULL,
    title            VARCHAR(255) NOT NULL,
    description      VARCHAR(255) NOT NULL,
    id_user          INTEGER      NOT NULL,
    quantity         INTEGER      NOT NULL,
    price            INTEGER      NOT NULL,
    location         VARCHAR(255) NOT NULL,
    image_url        VARCHAR(255) ,
    id_categorie_post INTEGER      NOT NULL,
    id_currency      INTEGER      NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    foreign key (id_type_post) references type_post(id)
);

-- Table des statuts
-- Gère les différents états possibles (ex: en cours, terminé...)
create table "status"(
    id               SERIAL PRIMARY KEY,
    status           VARCHAR(50)  NOT NULL,
    expiration       INTEGER      NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des conversations
-- Gère les discussions entre utilisateurs
CREATE table "chat"(
    id               SERIAL PRIMARY KEY,
    id_post          INTEGER      NOT NULL,
    id_status        INTEGER      NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    foreign key (id_status) references status(id)
);

-- Table des types de messages
-- Définit les différents types de messages possibles
CREATE table "type_message"(
    id               SERIAL PRIMARY KEY,
    type             VARCHAR(50)  NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des messages
-- Stocke les messages échangés entre utilisateurs
Create table  "message"(
    id               SERIAL PRIMARY KEY,
    message          VARCHAR(255) NOT NULL,
    id_user          INTEGER      NOT NULL,
    id_chat          INTEGER      NOT NULL,
    id_type_message  INTEGER      NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des types de documents PDF
-- Catégorise les différents types de documents
create table "type_pdf"(
    id               SERIAL PRIMARY KEY,
    type             VARCHAR(50)  NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des documents PDF
-- Stocke les documents PDF associés aux transactions
create table "pdf"(
    id               SERIAL PRIMARY KEY,
    pdf              VARCHAR(255) NOT NULL,
    id_post          INTEGER      NOT NULL,
    id_user          INTEGER      NOT NULL,
    id_type_pdf      INTEGER      NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Password table relationships
ALTER TABLE "password"
    ADD CONSTRAINT fk_password_user
        FOREIGN KEY (id_user)
            REFERENCES "user" (id);

-- Post table relationships
ALTER TABLE "post"
    ADD CONSTRAINT fk_post_type_post
        FOREIGN KEY (id_type_post)
            REFERENCES "type_post" (id),
    ADD CONSTRAINT fk_post_user
        FOREIGN KEY (id_user)
            REFERENCES "user" (id),
    ADD CONSTRAINT fk_post_categorie_post
        FOREIGN KEY (id_categorie_post)
            REFERENCES "categorie_post" (id),
    ADD CONSTRAINT fk_post_currency
        FOREIGN KEY (id_currency)
            REFERENCES "currency" (id);

-- Product table relationships
ALTER TABLE "product"
    ADD CONSTRAINT fk_product_unit
        FOREIGN KEY (id_unit)
            REFERENCES "unit" (id);

-- Chat table relationships
ALTER TABLE "chat"
    ADD CONSTRAINT fk_chat_post
        FOREIGN KEY (id_post)
            REFERENCES "post" (id);

-- Message table relationships
ALTER TABLE "message"
    ADD CONSTRAINT fk_message_user
        FOREIGN KEY (id_user)
            REFERENCES "user" (id),
    ADD CONSTRAINT fk_message_chat
        FOREIGN KEY (id_chat)
            REFERENCES "chat" (id),
    ADD CONSTRAINT fk_message_type_message
        FOREIGN KEY (id_type_message)
            REFERENCES "type_message" (id);

-- PDF table relationships
ALTER TABLE "pdf"
    ADD CONSTRAINT fk_pdf_post
        FOREIGN KEY (id_post)
            REFERENCES "post" (id),
    ADD CONSTRAINT fk_pdf_user
        FOREIGN KEY (id_user)
            REFERENCES "user" (id),
    ADD CONSTRAINT fk_pdf_type_pdf
        FOREIGN KEY (id_type_pdf)
            REFERENCES "type_pdf" (id);


-- Table des avis
-- Permet aux utilisateurs de s'évaluer mutuellement
CREATE TABLE "review"
(
    id           SERIAL PRIMARY KEY,
    id_user_from INTEGER NOT NULL,
    id_user_to   INTEGER NOT NULL,
    rating       INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment      TEXT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_review_user_from FOREIGN KEY (id_user_from) REFERENCES "user" (id),
    CONSTRAINT fk_review_user_to FOREIGN KEY (id_user_to) REFERENCES "user" (id)
);

-- Table des favoris
-- Permet aux utilisateurs de sauvegarder leurs publications préférées
CREATE TABLE "favorite"
(
    id         SERIAL PRIMARY KEY,
    id_user    INTEGER NOT NULL,
    id_post    INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_favorite_user FOREIGN KEY (id_user) REFERENCES "user" (id),
    CONSTRAINT fk_favorite_post FOREIGN KEY (id_post) REFERENCES "post" (id),
    CONSTRAINT unique_favorite UNIQUE (id_user, id_post)
);


-- Table des signalements
-- Permet de signaler du contenu inapproprié
CREATE TABLE "report"
(
    id         SERIAL PRIMARY KEY,
    id_user    INTEGER      NOT NULL,
    id_post    INTEGER,
    id_message INTEGER,
    reason     VARCHAR(255) NOT NULL,
    status     VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_report_user FOREIGN KEY (id_user) REFERENCES "user" (id),
    CONSTRAINT fk_report_post FOREIGN KEY (id_post) REFERENCES "post" (id),
    CONSTRAINT fk_report_message FOREIGN KEY (id_message) REFERENCES "message" (id),
    CONSTRAINT check_report_target CHECK (
        (id_post IS NOT NULL AND id_message IS NULL) OR
        (id_post IS NULL AND id_message IS NOT NULL)
        )
);


-- Table des tags
-- Mots-clés pour catégoriser les publications
CREATE TABLE "tag"
(
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table de liaison posts-tags
-- Associe les tags aux publications
CREATE TABLE "post_tag"
(
    id_post    INTEGER NOT NULL,
    id_tag     INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_post, id_tag),
    CONSTRAINT fk_post_tag_post FOREIGN KEY (id_post) REFERENCES "post" (id),
    CONSTRAINT fk_post_tag_tag FOREIGN KEY (id_tag) REFERENCES "tag" (id)
);

-- Table des notifications
-- Gère les notifications des utilisateurs
CREATE TABLE "notification"
(
    id                SERIAL PRIMARY KEY,
    id_user           INTEGER      NOT NULL,
    message           VARCHAR(255) NOT NULL,
    is_read           BOOLEAN   DEFAULT FALSE,
    notification_type VARCHAR(50)  NOT NULL,
    reference_id      INTEGER,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notification_user FOREIGN KEY (id_user) REFERENCES "user" (id)
);
--

COMMENT ON TABLE "categorie_user" IS 'Définit les différentes catégories d''utilisateurs du système';

COMMENT ON TABLE "user" IS 'Stocke les informations principales des utilisateurs (nom, email, etc.)';

COMMENT ON TABLE "password" IS 'Gère les mots de passe des utilisateurs (séparé de la table user pour la sécurité)';

COMMENT ON TABLE "type_post" IS 'Catégorise les types de publications (vente, achat, échange, etc.)';

COMMENT ON TABLE "categorie_post" IS 'Classifie les publications par catégories (électronique, vêtements, etc.)';

COMMENT ON TABLE "currency" IS 'Liste les devises disponibles pour les transactions';

COMMENT ON TABLE "unit" IS 'Définit les unités de mesure utilisées pour les produits';

COMMENT ON TABLE "product" IS 'Catalogue des produits avec leurs unités de mesure';

COMMENT ON TABLE "post" IS 'Contient toutes les annonces publiées par les utilisateurs';

COMMENT ON TABLE "chat" IS 'Gère les conversations liées aux publications';

COMMENT ON TABLE "type_message" IS 'Catégorise les types de messages (texte, image, etc.)';

COMMENT ON TABLE "message" IS 'Contient tous les messages échangés dans les conversations';

COMMENT ON TABLE "status" IS 'Définit les différents états possibles avec leur durée de validité';

COMMENT ON TABLE "type_pdf" IS 'Classifie les types de documents PDF (factures, contrats, etc.)';

COMMENT ON TABLE "pdf" IS 'Stocke les documents PDF liés aux publications et utilisateurs';

COMMENT ON TABLE "review" IS 'Système d''évaluation entre utilisateurs avec commentaires';

COMMENT ON TABLE "favorite" IS 'Gère les publications favorites des utilisateurs';

COMMENT ON TABLE "report" IS 'Système de signalement pour le contenu inapproprié';

COMMENT ON TABLE "tag" IS 'Mots-clés pour faciliter la recherche de publications';

COMMENT ON TABLE "post_tag" IS 'Associe les tags aux publications (relation many-to-many)';

COMMENT ON TABLE "notification" IS 'Système de notifications pour tenir les utilisateurs informés';
