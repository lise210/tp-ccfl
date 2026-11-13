# MCD

## Entités

### Site
- Propriétés : `code_site`, `nom`, `commune`, `annee_ouverture`, `surface_m2`
- Clé primaire : `code_site`

### Matériel
- Propriétés : `id_materiel`, `reference`, `designation`, `categorie`, `etat`, `annee_achat`, `valeur_achat`
- Clé primaire : `id_materiel`

### Association
- Propriétés : `id_association`, `nom`, `type_association`, `commune`, `code_postal`, `date_convention`, `convention_active`
- Clé primaire : `id_association`

### Réservation
- Propriétés : `id_reservation`, `quantite`, `date_debut`, `date_fin_prevue`, `date_retour_reelle`
- Clé primaire : `id_reservation`

## Relations et cardinalités

- Un site stocke zéro à plusieurs matériels
- Chaque matériel est rattaché à un seul site.  
  `Site (0,N) — stocke — Matériel (1,1)`

- Un site peut rattacher zéro à plusieurs associations
- Chaque association dépend d’un seul site.  
  `Site (0,N) — rattache — Association (1,1)`

- Un matériel peut figurer dans zéro à plusieurs réservations 
- Chaque réservation concerne un seul matériel.  
  `Matériel (0,N) — concerne — Réservation (1,1)`

- Une association peut effectuer zéro à plusieurs réservations
- Chaque réservation est faite par une seule association.  
  `Association (0,N) — effectue — Réservation (1,1)`

- Un site peut être le lieu de retrait de zéro à plusieurs réservations
- Chaque réservation est rattachée à un seul site.  
  `Site (0,N) — lieu de retrait — Réservation (1,1)`

# MLD
**clé primaire**
#clé étrangère

Site (<u>code_site</u>: CHAR(7), nom: TEXT, commune: TEXT, annee_ouverture: INTEGER, surface_m2: INTEGER)

Materiel (<u>id_materiel</u>: INTEGER, reference: TEXT, designation: TEXT, categorie: TEXT, etat: TEXT, annee_achat: INTEGER, valeur_achat: NUMERIC(8,2), #code_site: CHAR(7))

Association (<u>id_association</u>: INTEGER, nom: TEXT, type_association: TEXT, commune: TEXT, code_postal: TEXT, date_convention: DATE, convention_active: BOOLEAN, #code_site: CHAR(7))

Reservation (<u>id_reservation</u>: CHAR(7), quantite: INTEGER, date_debut: DATE, date_fin_prevue: DATE, date_retour_reelle: DATE, #id_materiel: INTEGER, #id_association: INTEGER, #code_site: CHAR(7))

les valeurs nullables : annee_achat, valeur_achat, code_postal et date_retour_reelle

# Justifications

La clé primaire de `Reservation` est de type texte, car les identifiants sont de la forme `R250000` et contiennent une lettre. Le type `CHAR(7)` conserve leur format fixe.

`valeur_achat` sera stockée en `NUMERIC(8,2)` pour représenter les montants en € avec leurs centimes. Un flottant peut introduire de petites erreurs d’arrondi.

La colonne `convention_active`, binaire sous la forme `oui` ou `non`, sera convertie en booléen : `TRUE` pour `oui` et `FALSE` pour `non`.

`date_retour_reelle` doit accepter une valeur nulle. Une date absente indique que le prêt est encore en cours, et non que la donnée est erronée.

Le `code_site` de `materiel` indique le site où le matériel est stocké <br>
Le `code_site` de `association` indique le site auquel elle est rattachée <br>
=> ces informations ont des rôles différents. <br>
Le `code_site` de `reservation` indique le lieu de retrait. <br>
l’énoncé demande une clé étrangère de `reservation` vers `site`.
