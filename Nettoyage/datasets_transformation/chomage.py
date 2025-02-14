import pandas as pd
import os 

def nettoyer_chomage(fichier_entree,dossier_sortie):
    try:

        df = pd.read_csv(fichier_entree, delimiter = ';' , dtype = str)
        print(df.info())
        df = df.dropna()
        df = df.drop_duplicates()

        # Nettoyer la colonne 'taux de chomage'
        # Supprimer les caractères indésirables (comme (SD) ou (A))
        df['taux de chomage'] = df['taux de chomage'].str.replace(r'[^0-9,]', '', regex=True)

        df = df[df['Année'] >= 2002]

        # Remplacer les virgules par des points pour la conversion en float
        df['taux de chomage'] = df['taux de chomage'].str.replace(',', '.').astype(float)

        # Extraire l'année de la colonne 'Période'
        df['Année'] = df['Période'].str.extract(r'(\d{4})').astype(int)

        # Calculer la moyenne du taux de chômage par année
        moyenne_par_annee = df.groupby('Année')['taux de chomage'].mean().reset_index()

        # Afficher le résultat
        print(moyenne_par_annee)

        # Sauvegarder le résultat dans un nouveau fichier CSV
        dossier_sortie = "Nettoyage/datasets_nettoyer"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "chomage_nettoyer.csv"
        chemin_sortie = os.path.join(dossier_sortie,nom_fichier)
        moyenne_par_annee.to_csv(chemin_sortie, index=False)

    except Exception as e:
        print(e)