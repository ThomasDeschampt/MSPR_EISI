import pandas as pd
import os 

def nettoyer_commiseriat(fichier_entree,dossier_sortie):
    try:

        df = pd.read_csv(fichier_entree, delimiter = ';' , dtype = str)
        print(df.info())
        df = df.dropna()
        df = df.drop_duplicates()

        df = df[['departement']]

        def est_departement_valide(departement):
            # Vérifie si le code département est un nombre (peut être sur 2 ou 3 chiffres pour les départements DOM)
            return departement.isdigit() and (int(departement) <= 95 or (int(departement) >= 971 and int(departement) <= 976))

        # Appliquer la validation à la colonne 'departement'
        df['departement'] = df['departement'].str.strip()  # Supprimer les espaces autour
        df = df[df['departement'].apply(est_departement_valide)]

        # Vérifier s'il reste des données après filtrage
        if df.empty:
            raise ValueError("Aucun département valide n'a été trouvé dans le fichier")

        # Création du nouveau csv nettoyé
        dossier_sortie = "Nettoyage/datasets_nettoyer"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        nom_fichier = "commiseriat_nettoyer.csv"
        chemin_sortie = os.path.join(dossier_sortie,nom_fichier)
        # Sauvegarder le fichier nettoyé
        df.to_csv(chemin_sortie, index=False, sep=';')
        print(f"Fichier nettoyé et sauvegardé : {chemin_sortie}")

    except Exception as e:
        print(e)