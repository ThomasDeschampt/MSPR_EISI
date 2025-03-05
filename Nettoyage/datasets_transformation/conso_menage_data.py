import pandas as pd
import os 

def nettoyer_conso_menage_data(fichier_entree,dossier_sortie):
    try:

        df = pd.read_csv(fichier_entree, delimiter = ';')
        print(df.info())
        df = df.drop_duplicates()

        #afficher les colonnes et le nombre de valeurs manquantes
        print(df.isnull().sum())

        # Supprimer les colonnes inutiles
        df = df.drop(columns=['REF_PERIOD_DETAIL'])
        df = df.drop(columns=['LAST_UPDATE'])
        df = df.drop(columns=['TABLE_IDENTIFIER'])

        df = df[df['TIME_PERIOD'] >= 2002]        

        # On va faire la moyenne des valeurs de REF_YEAR_PRICE pour les valeurs manquantes
        df['REF_YEAR_PRICE'] = df['REF_YEAR_PRICE'].fillna(df['REF_YEAR_PRICE'].mean())

        print(df.isnull().sum())

        # Création du nouveau csv nettoyé
        dossier_sortie = "Nettoyage/datasets_nettoyer"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "conso_menage_data.csv"
        chemin_sortie = os.path.join(dossier_sortie,nom_fichier)
        df.to_csv(chemin_sortie, index=False, sep=';')

    except Exception as e:
        print(e)