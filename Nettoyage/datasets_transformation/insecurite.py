import pandas as pd
import os 
import numpy as np
from sklearn.linear_model import LinearRegression

def nettoyer_insecurite(fichier_entree,dossier_sortie):
    try:

        df = pd.read_csv(fichier_entree, delimiter = ';')
        print(df.info())
        df = df.dropna()
        df = df.drop_duplicates()
        
        # On supprime les colonnes non pertinentes
        df = df.drop(columns=['Code_region'])
        df = df.drop(columns=['insee_pop_millesime'])
        df = df.drop(columns=['insee_log'])
        df = df.drop(columns=['insee_log_millesime'])
        df = df.drop(columns=['Code_departement'])


        # Moyenne par année
        df['taux_pour_mille'] = df['taux_pour_mille'].str.replace(',', '.').astype(float)
        moyenne_par_annee = df.groupby('annee')[['nombre', 'taux_pour_mille', 'insee_pop']].mean().reset_index()

        # Régression linéaire pour estimer les années manquantes à partir de 2002
        annee_min = 2002
        annee_max = 2024
        annees_existantes = moyenne_par_annee['annee'].values.reshape(-1, 1)

        # Liste des colonnes à prédire
        colonnes_a_predire = ['taux_pour_mille', 'nombre', 'insee_pop']
        predictions_dict = {}

        # entrianement des modèles de régression linéaire
        for colonne in colonnes_a_predire:
            valeurs_existantes = moyenne_par_annee[colonne].values.reshape(-1, 1)
            modele = LinearRegression()
            modele.fit(annees_existantes, valeurs_existantes)

            # Prédire les valeurs pour les années manquantes
            annees_manquantes = np.arange(annee_min, annee_max + 1).reshape(-1, 1)
            predictions = modele.predict(annees_manquantes)

            # Sauvegarder les prédictions dans le dictionnaire
            predictions_dict[colonne] = predictions.flatten()

        # Création d'un DataFrame pour les prédictions
        df_predictions = pd.DataFrame({
            'annee': annees_manquantes.flatten(),
            'taux_pour_mille': predictions_dict['taux_pour_mille'],
            'nombre': predictions_dict['nombre'],
            'insee_pop': predictions_dict['insee_pop']
        })

        # on fusionne les données existantes et les prédictions
        moyenne_par_annee = pd.concat([moyenne_par_annee, df_predictions]).drop_duplicates(subset=['annee']).sort_values(by='annee')

        # creation du nouveau csv nettoyé
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "insecurite.csv"
        chemin_sortie = os.path.join(dossier_sortie, nom_fichier)

        moyenne_par_annee.to_csv(chemin_sortie, index=False, sep=';')
        print(f"Le fichier a été sauvegardé sous {chemin_sortie}")

    except Exception as e:
        print(e)