import pandas as pd
import os

def nettoyer_valeurs_mensuelles(fichier_entree, fichier_sortie="valeurs_mensuelles_nettoyees.csv"):
    # Lire le fichier avec le bon séparateur et ignorer les 3 premières lignes
    df = pd.read_csv(fichier_entree, sep=";", skiprows=3, names=["periode", "valeur", "code"])

    # Supprimer les lignes vides ou incomplètes
    df = df.dropna(subset=["periode", "valeur"])

    # Convertir les valeurs
    df["valeur"] = df["valeur"].astype(float).round(2)

    # Convertir "periode" en datetime mensuel
    df["periode"] = pd.to_datetime(df["periode"], format="%Y-%m")

    # Dossier de sortie
    dossier_sortie = "Nettoyage/datasets_nettoyer"
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    # S'assurer que seul le nom du fichier est utilisé ici
    nom_fichier = os.path.basename(fichier_sortie)
    chemin_sortie = os.path.join(dossier_sortie, nom_fichier)

    df.to_csv(chemin_sortie, index=False, sep=";")

    return chemin_sortie, df
