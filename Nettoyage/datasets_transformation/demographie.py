import pandas as pd
import os 

def nettoyer_demographie(fichier_entree,dossier_sortie):
    try:

        df = pd.read_csv(fichier_entree, delimiter = ';')
        df = df.dropna()
        df = df.drop_duplicates()

        df = df[df['Année '] >= 2002]

        # on nettoie et converti des colonnes
        for col in ['Population au 1er janvier', 'Naissances vivantes', 'Décès', 'Solde naturel', 'Solde migratoire', 'Ajustement']:
            df[col] = df[col].str.replace(' ', '').str.replace(',', '.').str.replace('+', '').astype(float)

        # creation du nouveau csv nettoyé
        dossier_sortie = "Nettoyage/datasets_nettoyer"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "demographie_nettoyer.csv"
        
        chemin_sortie = os.path.join(dossier_sortie,nom_fichier)
        df.to_csv(chemin_sortie, index=False, sep=';')
        print(f"Fichier nettoyé et sauvegardé : {chemin_sortie}")

    except Exception as e:
        print(e)