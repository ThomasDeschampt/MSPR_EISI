import pandas as pd
import os
import numpy as np
from sklearn.linear_model import LinearRegression

def nettoyer_pib(fichier_entree,dossier_sortie):
    try:

        df = pd.read_csv(fichier_entree, delimiter = ';' , dtype = str)
        print(df.info())
        df = df.dropna()
        df = df.drop_duplicates()

        # On renommr la colonne période par année
        df = df.rename(columns={'Période': 'Année'})

        # On garde seulement les années après 2002    
        df['Année'] = df['Année'].astype(int)
        df = df[df['Année'] >= 2002]

        # On supprime la colonne codes
        df = df.drop(columns=['Codes'])

        # Régression linéaire pour estimer les valeurs manquantes jusqu'en 2024
        annee_min = 2002
        annee_max = 2024
        annees_existantes = df['Année'].values.reshape(-1, 1)
        valeurs_existantes = df['PIB'].values.reshape(-1, 1)

        # Entraînement du modèle de régression linéaire
        modele = LinearRegression()
        modele.fit(annees_existantes, valeurs_existantes)

        # Prédire les valeurs pour les années manquantes
        annees_manquantes = np.arange(annee_min, annee_max + 1).reshape(-1, 1)
        predictions = modele.predict(annees_manquantes)

        # Création d'un DataFrame pour les prédictions
        df_predictions = pd.DataFrame({
            'Année': annees_manquantes.flatten(),
            'PIB': predictions.flatten()
        })

        # Fusionner les données existantes et les prédictions
        df = pd.concat([df, df_predictions]).drop_duplicates(subset=['Année']).sort_values(by='Année')

        #On prend pas les valeurs apres la virgule
        df['PIB'] = df['PIB'].astype(int)

        # Création du nouveau csv nettoyé
        dossier_sortie = "Nettoyage/datasets_nettoyer"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "pib_nettoyer.csv"
        chemin_sortie = os.path.join(dossier_sortie,nom_fichier)
        df.to_csv(chemin_sortie, index=False, sep=';')

    except Exception as e:
        print(e)