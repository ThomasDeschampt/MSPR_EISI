import pandas as pd
import os

def nettoyer_valeurs_annuelles(fichier_entree, fichier_sortie="valeurs_annuelles_nettoyees.csv"):
    df = pd.read_csv(fichier_entree, sep=";", skiprows=3, names=["periode", "valeur", "code"])

    # on supprime les lignes vides ou incomplètes
    df = df.dropna(subset=["periode", "valeur"])

    # on converti les valeurs en float et arrondir à 2 décimales
    df["valeur"] = df["valeur"].astype(float).round(2)

    # on converti "periode" en datetime mensuel
    df["periode"] = pd.to_datetime(df["periode"], format="%Y-%m", errors="coerce")

    # on supprime les lignes avec des dates invalides
    df = df.dropna(subset=["periode"])

    # Extraire l'année
    df["annee"] = df["periode"].dt.year

    # on garde seulement les années de 2002 à 2024
    df = df[(df["annee"] >= 2002) & (df["annee"] <= 2024)]

    # on regroupe par année et on calcule la moyenne des valeurs
    df_annuel = df.groupby("annee", as_index=False)["valeur"].mean().round(2)

    # creation du nouveau csv nettoyé
    dossier_sortie = "Nettoyage/datasets_nettoyer"
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    nom_fichier = "consomenage.csv"
    chemin_sortie = os.path.join(dossier_sortie, nom_fichier)
    df_annuel.to_csv(chemin_sortie, index=False, sep=";")

    return chemin_sortie, df_annuel
