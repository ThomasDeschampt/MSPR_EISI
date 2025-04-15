import pandas as pd
import os
import numpy as np
from sklearn.linear_model import LinearRegression

def nettoyer_emplois_prive(fichier_entree, dossier_sortie):
    try:
        df = pd.read_csv(fichier_entree, delimiter=';')
        print(df.info())
        df = df.dropna()
        df = df.drop_duplicates()

        # on recupere l'annee de la periode
        df['Année'] = df['Période'].str.extract(r'(\d{4})').astype(int)

        # on calcule la moyenne par année
        moyenne_par_annee = df.groupby('Année')['Nombre de salariés'].mean().reset_index()

        # Régression linéaire pour estimer les années manquantes à partir de 2002
        annee_min = 2002
        annee_max = moyenne_par_annee['Année'].max()
        annees_existantes = moyenne_par_annee['Année'].values.reshape(-1, 1)
        valeurs_existantes = moyenne_par_annee['Nombre de salariés'].values.reshape(-1, 1)
        
        # Entraînement du modèle
        modele = LinearRegression()
        modele.fit(annees_existantes, valeurs_existantes)
        
        # Prédire les valeurs
        annees_manquantes = np.arange(annee_min, annee_max + 1).reshape(-1, 1)
        predictions = modele.predict(annees_manquantes)
        predictions = np.round(predictions, 2)
        
        # Création d'un DataFrame pour les prédictions
        df_predictions = pd.DataFrame({
            'Année': annees_manquantes.flatten(),
            'Nombre de salariés': predictions.flatten()
        })
        
        # on fusionne les données existantes et les prédictions
        df_final = pd.concat([moyenne_par_annee, df_predictions]).drop_duplicates(subset=['Année']).sort_values(by='Année')
        
        # creation du nouveau csv nettoyé
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)
        
        chemin_sortie = os.path.join(dossier_sortie, "emplois_prive_nettoyer.csv")
        df_final.to_csv(chemin_sortie, index=False, sep=';')

        print(f"Fichier sauvegardé à : {chemin_sortie}")
    except Exception as e:
        print(f"Erreur : {e}")