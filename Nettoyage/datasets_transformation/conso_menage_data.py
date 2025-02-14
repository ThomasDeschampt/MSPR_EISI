import pandas as pd
import os 

def nettoyer_conso_menage_data(fichier_entree,dossier_sortie):
    try:

        df = pd.read_csv(fichier_entree, delimiter = ';')
        print(df.info())
        df = df.drop_duplicates()

        df = df[df['TIME_PERIOD'] >= 2002]        

        # Création du nouveau csv nettoyé
        dossier_sortie = "Nettoyage/datasets_nettoyer"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "conso_menage_data.csv"
        chemin_sortie = os.path.join(dossier_sortie,nom_fichier)
        df.to_csv(chemin_sortie, index=False, sep=';')

    except Exception as e:
        print(e)