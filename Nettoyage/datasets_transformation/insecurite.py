import pandas as pd
import os 

def nettoyer_insecurite(fichier_entree,dossier_sortie):
    try:

        df = pd.read_csv(fichier_entree, delimiter = ';')
        print(df.info())
        df = df.dropna()
        df = df.drop_duplicates()

        # On supprime la colonne non pertinentes
        df = df.drop(columns=['Code_region'])
        df = df.drop(columns=['insee_pop_millesime'])
        df = df.drop(columns=['insee_log'])
        df = df.drop(columns=['insee_log_millesime'])
        df = df.drop(columns=['Code_departement'])


        # Moyenne par année
        df['taux_pour_mille'] = df['taux_pour_mille'].str.replace(',', '.').astype(float)
        moyenne_par_annee = df.groupby('annee')[['nombre', 'taux_pour_mille', 'insee_pop']].mean().reset_index()

        # Création du nouveau csv nettoyé
        dossier_sortie = "Nettoyage/datasets_nettoyer"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "insecurite.csv"
        chemin_sortie = os.path.join(dossier_sortie,nom_fichier)
        moyenne_par_annee.to_csv(chemin_sortie, index=False)

    except Exception as e:
        print(e)