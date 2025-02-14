import pandas as pd
import os

def nettoyer_depart_retraite(fichier_entree, dossier_sortie):
    try:
        print(f"Début du traitement du fichier : {fichier_entree}")
        
        # Charger le fichier CSV avec le bon séparateur
        df = pd.read_csv(fichier_entree, delimiter=';', dtype=str)
        
        # Supprimer les espaces inutiles dans les colonnes et les valeurs
        df.columns = df.columns.str.strip()
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        # Enlever les valeurs entre parenthèses
        df = df.replace(to_replace=r'\(.*?\)', value='', regex=True)
        
        # Renommer les colonnes pour éviter les caractères spéciaux
        df.rename(columns={
            'Âge conjoncturel de départ à la retraite': 'Age_depart',
            'Proportion de personnes fortement limitées au cours de la première année de retraite (%)': 'Proportion_fortement_limitees',
            'Proportion de personnes limitées, mais pas fortement au cours de la première année de retraite (%)': 'Proportion_limitees',
            'Proportion de retraités à 61 ans': 'Proportion_retraites_61ans',
            'Durée moyenne en emploi (hors cumul)': 'Duree_emploi',
            'Durée moyenne sans emploi ni retraite': 'Duree_sans_emploi'
        }, inplace=True)
        
        # Convertir les valeurs numériques en float
        colonnes_a_convertir = ['Proportion_fortement_limitees', 'Proportion_limitees', 'Age_depart', 'Proportion_retraites_61ans', 'Duree_emploi', 'Duree_sans_emploi']
        for col in colonnes_a_convertir:
            df[col] = df[col].str.replace(',', '.').astype(float)
        
        # Convertir la colonne année en int
        df['Annee'] = df['annee'].astype(int)
        
        # Supprimer les entrées avant 2002
        df = df[df['Annee'] >= 2002]
        
        # Supprimer les doublons
        df.drop_duplicates(inplace=True)
        
        # Définir le chemin de sortie
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)
        
        nom_fichier = "depart_retraite_nettoye.csv"
        chemin_sortie = os.path.join(dossier_sortie, nom_fichier)
        
        # Sauvegarder le fichier nettoyé
        df.to_csv(chemin_sortie, index=False, sep=';')
        print(f"Fichier nettoyé et sauvegardé : {chemin_sortie}")
    except Exception as e:
        print(f"Erreur lors du traitement de {fichier_entree} : {e}")
