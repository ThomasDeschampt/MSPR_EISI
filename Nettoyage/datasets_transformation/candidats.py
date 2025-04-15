import pandas as pd
import os 

def nettoyer_candidats(fichier_entree,dossier_sortie):
    try:

        df = pd.read_csv(fichier_entree, delimiter = ';' , dtype = str)
        print(df.info())
        df = df.drop_duplicates()

        # on remplace des virgules par des points et conversion en float
        df = df.apply(lambda x: x.str.replace(',', '.', regex=False) if x.dtype == "object" else x)

        # creation du nouveau csv nettoyé
        dossier_sortie = "Nettoyage/datasets_nettoyer"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "candidats_nettoyer.csv"
        chemin_sortie = os.path.join(dossier_sortie,nom_fichier)
        df.to_csv(chemin_sortie, index=False, sep=';')

    except Exception as e:
        print(e)