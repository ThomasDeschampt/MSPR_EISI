from prophet import Prophet
import pandas as pd
import numpy as np
from datetime import datetime

# Chargement des données
df = pd.read_csv('./Prediction/data/donnees_fusionnees.csv')

# Liste des variables à ne pas prédire
variables_a_ne_pas_predire = ['Tour', 'Pourcentage_Abstention', 'Pourcentage_Votants', 'Ratio_voix_exprime']

# Préparation du dataframe pour les prédictions futures
future_years = pd.DataFrame({'Annee': [2025, 2026, 2027, 2028]})
results = future_years.copy()

# On va boucler sur les colonnes du dataframe pour prédire chaque variable
for colonne in df.columns:
    if colonne not in variables_a_ne_pas_predire and colonne != 'Annee':
        print(f"\nPrédiction en cours pour: {colonne}")
        
        try:
            # Préparation des données pour Prophet
            prophet_df = df[['Annee', colonne]].dropna().copy()
            
            # On ne garde que la première ligne de chaque année
            prophet_df = prophet_df.groupby('Annee').first().reset_index()
            
            # Vérifier qu'il y a assez de données
            if len(prophet_df) < 2:
                print(f"Pas assez de données pour {colonne} - seulement {len(prophet_df)} points")
                results[colonne] = np.nan
                continue
                
            # Convertir l'année en datetime
            prophet_df['ds'] = pd.to_datetime(prophet_df['Annee'], format='%Y')
            prophet_df['y'] = prophet_df[colonne]
            
            # Création et entraînement du modèle
            model = Prophet(
                yearly_seasonality=True,
                seasonality_mode='additive',
                changepoint_prior_scale=0.05
            )
            model.fit(prophet_df)
                           
            # Création du dataframe futur
            future = pd.DataFrame({
                'ds': pd.to_datetime(['2025-12-31', '2026-12-31', '2027-12-31', '2028-12-31'])
            })
            
            # Prédiction
            forecast = model.predict(future)
            
            # Filtrer spécifiquement pour les années 2025-2027
            forecast['year'] = forecast['ds'].dt.year
            predictions = forecast[forecast['year'].isin([2025, 2026, 2027, 2028])].copy()
            print(predictions)
            
            # Vérifier que nous avons bien 4 prédictions
            if len(predictions) != 4:
                print(f"Problème avec les années de prédiction - obtenu {predictions['year'].tolist()}")
                results[colonne] = np.nan
                continue
                
            # Trier par année et ajouter les prédictions
            predictions = predictions.sort_values('year')
            print(predictions[['ds', 'yhat']])
            
            # Ajouter les prédictions au dataframe results
            results[colonne] = predictions['yhat'].values
            results[colonne] = np.round(predictions['yhat'].values, 2)
            
            print(f"Prédictions réussies pour {colonne}: {predictions['yhat'].values}")
            
        except Exception as e:
            print(f"Erreur lors de la prédiction pour {colonne}: {str(e)}")
            results[colonne] = np.nan

# Affichage des résultats
print("\nRésultats finaux des prédictions:")
print(results)

# Création des colonnes pour les bords politiques
bords_politiques = ['Bord_Centre', 'Bord_Droite', 'Bord_Extrêmedroite', 'Bord_Extrêmegauche', 'Bord_Gauche']

# Duplication de chaque année 10 fois (2 tours × 5 bords politiques)
results_expanded = pd.DataFrame()
for annee in results['Annee'].unique():
    for tour in [1]:  # Ajout des deux tours
        for i, bord in enumerate(bords_politiques):
            temp = results[results['Annee'] == annee].copy()
            temp['Tour'] = tour  # Ajout de la colonne Tour
            for b in bords_politiques:
                temp[b] = False
            temp[bord] = True
            results_expanded = pd.concat([results_expanded, temp], ignore_index=True)

# Réorganisation des colonnes
cols = ['Annee', 'Tour'] + [c for c in results.columns if c not in ['Annee', 'Tour']] + bords_politiques
results_expanded = results_expanded[cols]

tour_index = cols.index('Tour')

#On supprime la colonne 'Bord'
results_expanded = results_expanded.drop(columns='Bord')
#On supprime la colonne 'Bord'
results_expanded = results_expanded.drop(columns='Parti')

results_expanded = results_expanded.round(2)

# Affichage des résultats finaux
print("\nRésultats finaux des prédictions avec bords politiques:")
print(results_expanded)

# Sauvegarde des résultats
results_expanded.to_csv('./Prediction/data/predictions_2025_2027.csv', index=False)
print("\nPrédictions sauvegardées dans './Prediction/data/predictions_2025_2027.csv'")