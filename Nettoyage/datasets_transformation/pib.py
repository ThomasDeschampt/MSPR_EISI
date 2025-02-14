import pandas as pd
import os 

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

        # Création du nouveau csv nettoyé
        dossier_sortie = "Nettoyage/datasets_nettoyer"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "pib_nettoyer.csv"
        chemin_sortie = os.path.join(dossier_sortie,nom_fichier)
        df.to_csv(chemin_sortie, index=False)

    except Exception as e:
        print(e)