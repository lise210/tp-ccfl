import csv
from collections import Counter

CHEMIN_SITES = "data/sites.csv"
CHEMIN_RESERVATIONS = "data/reservations.csv"
CHEMIN_MATERIEL = "data/materiel.csv"
CHEMIN_ASSOCIATIONS = "data/associations.csv"


def lire_csv(chemin):
    with open(chemin, encoding="utf-8", newline="") as fichier:
        return list(csv.DictReader(fichier))


def compter_par(lignes, colonne):
    """Récup la valeur de la colonne pour chaque ligne. Counter compte les occurrences de chaque valeur"""
    return dict(Counter(ligne[colonne] for ligne in lignes)) #Counter compte combien de fois chaque valeur apparaît.

def total_par(lignes, colonne_groupe, colonne_valeur):
    """Additionne les valeurs entières pour chaque groupe"""
    totaux = {}
    for ligne in lignes:
        groupe = ligne[colonne_groupe]
        valeur = int(ligne[colonne_valeur])
        if groupe not in totaux:
            totaux[groupe] = 0
        totaux[groupe] = totaux[groupe] + valeur
    return totaux

class Site:
    def __init__(self, code_site, nom, commune, annee_ouverture, surface_m2):
        self.code_site = code_site
        self.nom = nom
        self.commune = commune
        self.annee_ouverture = int(annee_ouverture)
        self.surface_m2 = int(surface_m2)
    
    def anciennete(self, annee_reference):
        """Renvoie le nombre d'années depuis l'ouverture"""
        return (annee_reference - self.annee_ouverture)
    
    def __str__(self):
        """renvoie une ligne lisible, par exemple POL-HAZ - Pole technique d'Hazebrouck (Hazebrouck), 1800 m2"""
        return (f"{self.code_site} - {self.nom} ({self.commune}), {self.surface_m2} m2")

def reservations_en_cours(reservations):
    """Renvoie les réservations sans date de retour réelle"""
    en_cours = []
    for ligne in reservations:
        if not ligne["date_retour_reelle"].strip():
            en_cours.append(ligne)
    return en_cours

def main():
    sites = lire_csv(CHEMIN_SITES)
    materiel = lire_csv(CHEMIN_MATERIEL)
    associations = lire_csv(CHEMIN_ASSOCIATIONS)
    reservations = lire_csv(CHEMIN_RESERVATIONS)

    print("Nombre de sites :", len(sites))
    print("Nombre de matériels :", len(materiel))
    print("Nombre d'associations :", len(associations))
    print("Nombre de réservations :", len(reservations))

    print("\nSites et ancienneté pour 2026 :")
    for ligne in sites:
        site = Site(
            ligne["code_site"],
            ligne["nom"],
            ligne["commune"],
            ligne["annee_ouverture"],
            ligne["surface_m2"])
        print(f"{site} — ancienneté : {site.anciennete(2026)} ans")

    reservations_par_site = compter_par(reservations, "code_site")
    print("\nNombre de réservations par site, ordre décroissant :")
    """J'ai dû chhercher comment utiliser sorted avec un dictionnaire, donc :
    # .items() : récupère les couples (clé, valeur).
    # key=lambda x: x[0] : trie par clé.
    # key=lambda x: x[1] : trie par valeur."""
    for code_site, nombre in sorted(reservations_par_site.items(), key=lambda element: element[1], reverse=True):
        print(f"{code_site} : {nombre}")

    quantites_par_site = total_par(reservations, "code_site", "quantite")
    print("\nQuantité totale réservée par site, ordre décroissant :")
    for code_site, quantite in sorted(quantites_par_site.items(), key=lambda element: element[1], reverse=True):
        print(f"{code_site} : {quantite}")

    print("\nNombre de matériels par état :")
    for etat, nombre in compter_par(materiel, "etat").items():
        print(f"{etat} : {nombre}")

    categories = compter_par(materiel, "categorie")
    print("\nNombre de catégories distinctes :", len(categories))

    en_cours = reservations_en_cours(reservations)
    print("Nombre de réservations en cours :", len(en_cours))

if __name__ == "__main__":
    main()