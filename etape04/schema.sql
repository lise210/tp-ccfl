-- Création de la BDD, dans le le terminal : createdb ccfl
-- Exécution depuis la racine du projet : psql -d ccfl -f etape04/schema.sql

-- Table des sites
CREATE TABLE IF NOT EXISTS site (
    code_site CHAR(7) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    commune VARCHAR(100) NOT NULL,
    annee_ouverture INT NOT NULL,
    surface_m2 INT NOT NULL);

-- Table du matériel
CREATE TABLE IF NOT EXISTS materiel (
    id_materiel INT PRIMARY KEY,
    reference VARCHAR(20) NOT NULL,
    designation VARCHAR(150) NOT NULL,
    categorie VARCHAR(50) NOT NULL,
    etat VARCHAR(30) NOT NULL,
    annee_achat INT,
    code_site CHAR(7) NOT NULL,
    valeur_achat NUMERIC(8, 2),
    CONSTRAINT fk_materiel_site FOREIGN KEY (code_site) REFERENCES site(code_site));

-- Table des associations
CREATE TABLE IF NOT EXISTS association (
    id_association INT PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    type_association VARCHAR(50) NOT NULL,
    commune VARCHAR(100) NOT NULL,
    code_postal VARCHAR(10),
    date_convention DATE NOT NULL,
    code_site CHAR(7) NOT NULL,
    convention_active BOOLEAN NOT NULL,
    CONSTRAINT fk_association_site FOREIGN KEY (code_site) REFERENCES site(code_site));

-- Table des réservations
CREATE TABLE IF NOT EXISTS reservation (
    id_reservation CHAR(7) PRIMARY KEY,
    id_materiel INT NOT NULL,
    id_association INT NOT NULL,
    code_site CHAR(7) NOT NULL,
    quantite INT NOT NULL,
    date_debut DATE NOT NULL,
    date_fin_prevue DATE NOT NULL,
    date_retour_reelle DATE,
    CONSTRAINT fk_reservation_materiel FOREIGN KEY (id_materiel) REFERENCES materiel(id_materiel),
    CONSTRAINT fk_reservation_association FOREIGN KEY (id_association) REFERENCES association(id_association),
    CONSTRAINT fk_reservation_site FOREIGN KEY (code_site) REFERENCES site(code_site),
    CONSTRAINT chk_reservation_dates CHECK (date_fin_prevue >= date_debut),
    CONSTRAINT chk_reservation_quantite CHECK (quantite > 0));

-- Index pour les analyses et regroupements par site
CREATE INDEX IF NOT EXISTS idx_reservation_code_site ON reservation(code_site);

-- Index pour les analyses des matériels les plus réservés
CREATE INDEX IF NOT EXISTS idx_reservation_id_materiel ON reservation(id_materiel);

-- Index pour les analyses par mois de début de réservation
CREATE INDEX IF NOT EXISTS idx_reservation_date_debut ON reservation(date_debut);