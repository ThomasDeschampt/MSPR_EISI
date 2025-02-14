import pandas as pd
import os

def nettoyer_masse_salariale(fichier_entree, dossier_sortie):
    try:
        print(f"Début du traitement du fichier : {fichier_entree}")
        
        # Charger le fichier CSV avec le bon séparateur
        df = pd.read_csv(fichier_entree, delimiter=';', dtype=str)
        
        # Supprimer les espaces inutiles dans les colonnes et les valeurs
        df.columns = df.columns.str.strip()
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        # Convertir les colonnes numériques avec des virgules en float
        colonnes_a_convertir = ['Masse salariale à T+50 jours (brut)', 'Masse salariale à T+70 jours (brut)',
                                'Masse salariale à T+50 jours (cvs)', 'Masse salariale à T+70 jours (cvs)',
                                'Glissement trimestriel - Masse salariale à T+50 jours (cvs)',
                                'Glissement trimestriel - Masse salariale à T+70 jours (cvs)',
                                'Glissement annuel - Masse salariale à T+50 jours (cvs)',
                                'Glissement annuel - Masse salariale à T+70 jours (cvs)']
        for col in colonnes_a_convertir:
            df[col] = df[col].str.replace(',', '.').astype(float)
        
        # Convertir la colonne année en int
        df['Année'] = df['Année'].astype(int)
        
        # Supprimer les entrées avant 2002
        df = df[df['Année'] >= 2002]
        
        # Supprimer les doublons
        df.drop_duplicates(inplace=True)
        
        # Définir le chemin de sortie
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)
        
        nom_fichier = "masse_salariale_nettoyee.csv"
        chemin_sortie = os.path.join(dossier_sortie, nom_fichier)
        
        # Sauvegarder le fichier nettoyé
        df.to_csv(chemin_sortie, index=False, sep=';')
        print(f"Fichier nettoyé et sauvegardé : {chemin_sortie}")
    except Exception as e:
        print(f"Erreur lors du traitement de {fichier_entree} : {e}")
