import pandas as pd
import os

def nettoyer_valeurs_annuelles(fichier_entree, fichier_sortie="valeurs_annuelles_nettoyees.csv"):
    # Lire le fichier avec le bon séparateur et ignorer les 3 premières lignes
    df = pd.read_csv(fichier_entree, sep=";", skiprows=3, names=["periode", "valeur", "code"])

    # Supprimer les lignes vides ou incomplètes
    df = df.dropna(subset=["periode", "valeur"])

    # Convertir les valeurs en float et arrondir à 2 décimales
    df["valeur"] = df["valeur"].astype(float).round(2)

    # Convertir "periode" en datetime mensuel
    df["periode"] = pd.to_datetime(df["periode"], format="%Y-%m", errors="coerce")

    # Supprimer les lignes avec des dates invalides
    df = df.dropna(subset=["periode"])

    # Extraire l'année
    df["annee"] = df["periode"].dt.year

    # Garder seulement les années de 2002 à 2024
    df = df[(df["annee"] >= 2002) & (df["annee"] <= 2024)]

    # Grouper par année et faire la moyenne (ou somme si tu préfères)
    df_annuel = df.groupby("annee", as_index=False)["valeur"].mean().round(2)

    # Dossier de sortie
    dossier_sortie = "Nettoyage/datasets_nettoyer"
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    # Créer le chemin complet du fichier de sortie
    nom_fichier = os.path.basename(fichier_sortie)
    chemin_sortie = os.path.join(dossier_sortie, nom_fichier)

    # Sauvegarder au format CSV
    df_annuel.to_csv(chemin_sortie, index=False, sep=";")

    return chemin_sortie, df_annuel
