import pandas as pd
import os 

def nettoyer_chomage(fichier_entree,dossier_sortie):
    try:

        df = pd.read_csv(fichier_entree, delimiter = ';' , dtype = str)
        print(df.info())
        df = df.dropna()
        df = df.drop_duplicates()

        # On nettoie la colonne 'taux de chomage'
        df['taux de chomage'] = df['taux de chomage'].str.replace(r'[^0-9,]', '', regex=True)

        # Remplacement des virgules par des points et conversion en float
        df['taux de chomage'] = df['taux de chomage'].str.replace(',', '.').astype(float)

        # On récupère l'année sans le trimestre
        df['Année'] = df['Période'].str.extract(r'(\d{4})').astype(int)

        # On garde seulement les années après 2002
        df = df[df['Année'] >= 2002]
        
        # Moyenne par année
        moyenne_par_annee = df.groupby('Année')['taux de chomage'].mean().reset_index()
        

        # Création du nouveau csv nettoyé
        dossier_sortie = "Nettoyage/datasets_nettoyer"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "chomage_nettoyer.csv"
        chemin_sortie = os.path.join(dossier_sortie,nom_fichier)
        moyenne_par_annee.to_csv(chemin_sortie, index=False)

    except Exception as e:
        print(e)