import pandas as pd
import os
import numpy as np
from sklearn.linear_model import LinearRegression

def nettoyer_retraite(fichier_entree, dossier_sortie):
    try:
        df = pd.read_csv(fichier_entree, delimiter=';', dtype=str)
        print(df.info())

        # on supprimes les lignes avec des valeurs manquantes et doublons
        df = df.dropna()
        df = df.drop_duplicates()

        # on renomme la colonne 'Retraite'
        df = df.rename(columns={'Retraite': 'Taux_Retraite'})

        # On garde seulement les années après 2004
        df['Année'] = df['Année'].astype(int)
        df = df[df['Année'] >= 2004]

        # Régression linéaire pour estimer les valeurs manquantes jusqu'en 2024
        annee_min = 2002
        annee_max = 2024
        annees_existantes = df['Année'].values.reshape(-1, 1)
        valeurs_existantes = df['Taux_Retraite'].values.reshape(-1, 1)

        # Entraînement du modèle
        modele = LinearRegression()
        modele.fit(annees_existantes, valeurs_existantes)

        # Prédire les valeurs
        annees_manquantes = np.arange(annee_min, annee_max + 1).reshape(-1, 1)
        predictions = modele.predict(annees_manquantes)

        # Création d'un DataFrame pour les prédictions
        df_predictions = pd.DataFrame({
            'Année': annees_manquantes.flatten(),
            'Taux_Retraite': predictions.flatten()
        })

        # on fusionne les données existantes et les prédictions
        df = pd.concat([df, df_predictions]).drop_duplicates(subset=['Année']).sort_values(by='Année')

        # on garde juste deux chiffres après la virgule
        df['Taux_Retraite'] = df['Taux_Retraite'].astype(float).round(2)

        # creation du nouveau csv nettoyé
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "retraite_nettoyer.csv"
        chemin_sortie = os.path.join(dossier_sortie, nom_fichier)
        df.to_csv(chemin_sortie, index=False, sep=';')

    except Exception as e:
        print(e)
