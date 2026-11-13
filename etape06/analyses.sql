-- Question 1. Par site (code_site, nom) : nombre de réservations, quantité totale réservée et nombre d'associations distinctes, trié par nombre de réservations décroissant. Les sites sans réservation doivent apparaître avec 0.
SELECT
    s.code_site,
    s.nom,
    COUNT(r.id_reservation) AS nb_reservations,
    COALESCE(SUM(r.quantite), 0) AS qtt_totale,
    COUNT(DISTINCT r.id_association) AS nb_associations
FROM site s
LEFT JOIN reservation r 
    ON r.code_site = s.code_site
GROUP BY s.code_site, s.nom
ORDER BY nb_reservations DESC;


-- Question 2. Nombre de réservations par mois de date_debut, au format AAAA-MM, trié chronologiquement.
SELECT
    TO_CHAR(date_debut, 'YYYY-MM') AS mois,
    COUNT(*) AS nb_reservations
FROM reservation
GROUP BY TO_CHAR(date_debut, 'YYYY-MM')
ORDER BY mois;


-- Question 3. Les 10 matériels les plus réservés (id_materiel, designation, categorie, nombre de réservations).
SELECT
    m.id_materiel,
    m.designation,
    m.categorie,
    COUNT(r.id_reservation) AS nb_reservations
FROM materiel m
JOIN reservation r 
    ON r.id_materiel = m.id_materiel
GROUP BY m.id_materiel, m.designation, m.categorie
ORDER BY nb_reservations DESC, m.id_materiel
LIMIT 10;


-- Question 4. Taux de retard en pourcentage, arrondi à deux décimales, globalement puis par site, calculé sur les seules réservations closes : un retard est un retour réel postérieur à la date de fin prévue.



-- Question 5. Les catégories dont le nombre de réservations est supérieur à la moyenne des catégories, avec ce nombre.
WITH reservations_par_categorie AS (
    SELECT
        m.categorie,
        COUNT(r.id_reservation) AS nb_reservations
    FROM materiel m
    LEFT JOIN reservation r 
        ON r.id_materiel = m.id_materiel
    GROUP BY m.categorie)
SELECT 
    categorie, 
    nb_reservations
FROM reservations_par_categorie
WHERE nb_reservations > (
    SELECT AVG(nb_reservations)
    FROM reservations_par_categorie)
ORDER BY nb_reservations DESC;
