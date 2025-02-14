import pandas as pd
import os 

def nettoyer_chomage(fichier_entree,dossier_sortie):
    try:

        df = pd.read_csv(fichier_entree, delimiter = ';' , dtype = str)

        df['taux de chommage'] = df ['taux de chommage'].str.replace(r'\(.*?\)', '', regex = True)
        df['taux de chomage'] = df['taux de chomage'].str.replace(',', '.').astype(float)

        df_moyenne = df.groupby('Année')['taux de chommage'].str.replace(',','.').astype(float)        
        print(df.info())
        df = df.dropna()
        df = df.drop_duplicates()

        dossier_sortie = "Nettoyage/datasets_nettoyer"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "chomage_nettoyer.csv"
        chemin_sortie = os.path.join(dossier_sortie,nom_fichier)

        df_moyenne.to_csv(chemin_sortie, index = False, sep = ';')
        print("caca")
    except Exception as e:
        print(e)