import pandas as pd


def main():
    df_sites = pd.read_csv("data/sites.csv")
    df_materiel = pd.read_csv("data/materiel.csv")
    df_associations = pd.read_csv("data/associations.csv")
    df_reservations = pd.read_csv("data/reservations.csv")

    # Convertit les trois colonnes de dates des réservations.
    for colonne in ["date_debut", "date_fin_prevue", "date_retour_reelle"]:
        df_reservations[colonne] = pd.to_datetime(df_reservations[colonne], format="%Y-%m-%d")

    print("\n----- Matériels ----")
    print("Dimensions :", df_materiel.shape)
    df_materiel.info()
    print("Valeurs manquantes par colonne :")
    print(df_materiel.isnull().sum())

    print("\n----- Réservations -----")
    print("Dimensions :", df_reservations.shape)
    df_reservations.info()
    print("Valeurs manquantes par colonne :")
    print(df_reservations.isnull().sum())

    print("\n----- Valeurs d'achat avant conversion :")
    print("Valeurs d'achat contenant une virgule :")
    for valeur in df_materiel["valeur_achat"].value_counts().index:
        if "," in valeur:
            print(valeur)
    # Je change la , en . et je convertie le type de la colonne
    df_materiel["valeur_achat"] = pd.to_numeric(df_materiel["valeur_achat"].str.replace(",", "."), errors="coerce")

    print("\n----- Type après conversion :", df_materiel["valeur_achat"].dtype)
    print("Valeurs d'achat manquantes après conversion :", df_materiel["valeur_achat"].isnull().sum())

    print("\n----- Les 10 matériels les plus chers :")
    materiel_par_prix = df_materiel.sort_values("valeur_achat", ascending=False)
    print(materiel_par_prix[["reference", "designation", "categorie", "valeur_achat"]].head(10))

    print("\n----- Nombre de matériels par catégorie :")
    print(df_materiel["categorie"].value_counts())

    print("\n----- Réservations et quantités par site et par nombre de réservations décroissant :")
    bilan_sites = df_reservations.groupby("code_site").agg(nombre_reservations=("id_reservation", "size"), quantite_totale=("quantite", "sum")    )
    print(bilan_sites.sort_values("nombre_reservations", ascending=False))

    # Retire les doublons stricts du matériel avant la joitnure
    materiel_sans_doublons = df_materiel.drop_duplicates()
    print("\n----- Nombre de matériels avant retrait des doublons :", len(df_materiel))
    print("\n----- Nombre après retrait des doublons :", len(materiel_sans_doublons))

    df_complet = df_reservations.merge(
        materiel_sans_doublons,
        on="id_materiel",
        how="left",
        suffixes=("", "_materiel"))
    df_complet = df_complet.merge(
        df_associations,
        on="id_association",
        how="left",
        suffixes=("", "_association"))
    print("\n----- Nombre de lignes après fusion :", len(df_complet))
    print("\n----- Réservations sans matériel correspondant :", df_complet["designation"].isnull().sum())


if __name__ == "__main__":
    main()