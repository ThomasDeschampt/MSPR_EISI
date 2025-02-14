import pandas as pd
import os 

def nettoyer_emplois_prive(fichier_entree,dossier_sortie):
    try:

        df = pd.read_csv(fichier_entree, delimiter = ';')
        print(df.info())
        df = df.dropna()
        df = df.drop_duplicates()

        # On récupère l'année sans le trimestre
        df['Année'] = df['Période'].str.extract(r'(\d{4})').astype(int)

        # Moyenne par année
        moyenne_par_annee = df.groupby('Année')['Nombre de salariés'].mean().reset_index()

        # Création du nouveau csv nettoyé
        dossier_sortie = "Nettoyage/datasets_nettoyer"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "emplois_prive_nettoyer.csv"
        chemin_sortie = os.path.join(dossier_sortie,nom_fichier)
        moyenne_par_annee.to_csv(chemin_sortie, index=False)

    except Exception as e:
        print(e)