import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Charger les données
df = pd.read_csv('./Prediction/data/donnees_preparees.csv')

# Filtrer les données pour le tour 1
df_tour1 = df[df['Tour'] == 1]

# Variables d'entrée (features) et variables de sortie (targets)
X = df_tour1.drop(columns=['Pourcentage_Abstention', 'Pourcentage_Votants', 'Ratio_voix_exprime'])
y = df_tour1[['Pourcentage_Abstention', 'Pourcentage_Votants', 'Ratio_voix_exprime']]

# Séparation des données en entraînement et test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalisation des données
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Modèle Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Prédictions sur le jeu de test
y_pred = model.predict(X_test_scaled)

# Évaluation du modèle
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Erreur absolue moyenne: {mae}')
print(f'Erreur quadratique moyenne: {mse}')
print(f'Coefficient de détermination R²: {r2}')


# Charger les données de prédiction (2025-2027)
df_pred = pd.read_csv('./Prediction/data/predictions_2025_2027.csv')

# Filtrer et préparer les variables d'entrée (en prenant les mêmes colonnes que pour l'entraînement)
X_pred = df_pred

# Normalisation des données (utiliser le même scaler que celui utilisé pendant l'entraînement)
X_pred_scaled = scaler.transform(X_pred)

# Effectuer les prédictions avec le modèle entraîné
y_pred_2025_2027 = model.predict(X_pred_scaled)

# Convertir les prédictions en DataFrame pour les afficher ou les sauvegarder
df_pred_predictions = pd.DataFrame(y_pred_2025_2027, columns=['Pourcentage_Abstention', 'Pourcentage_Votants', 'Ratio_voix_exprime'])

# Ajouter les prédictions au DataFrame original si vous souhaitez sauvegarder le fichier complet
df_pred = pd.concat([df_pred, df_pred_predictions], axis=1)

# Sauvegarder les prédictions dans un fichier CSV
df_pred.to_csv('./Prediction/data/predictions_2025_2027_with_predictions.csv', index=False)

# Afficher les premières lignes du résultat
print(df_pred.head())

# Charger les données avec prédictions
df_pred = pd.read_csv('./Prediction/data/predictions_2025_2027_with_predictions.csv')

# Vérifier les premières lignes du dataframe pour s'assurer qu'il est bien chargé
print(df_pred.head())

# Calculer la somme des valeurs de 'Ratio_voix_exprime' par année
sum_by_annee = df_pred.groupby('Annee')['Ratio_voix_exprime'].sum()

# Ajuster les valeurs de 'Ratio_voix_exprime' pour chaque année en utilisant un produit en croix
df_pred['Ratio_voix_exprime_adjusted'] = df_pred.apply(
    lambda row: row['Ratio_voix_exprime'] * (100 / sum_by_annee[row['Annee']]) 
    if sum_by_annee[row['Annee']] != 0 else 0, axis=1)

# Vérifier le résultat
print(df_pred[['Annee', 'Ratio_voix_exprime', 'Ratio_voix_exprime_adjusted']].head())

# Optionnel : Enregistrer le dataframe ajusté dans un nouveau fichier CSV
df_pred.to_csv('./Prediction/data/predictions_2025_2027_with_predictions_adjusted.csv', index=False)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Charger les données
df = pd.read_csv('./Prediction/data/predictions_2025_2027_with_predictions_adjusted.csv')

# Créer un dictionnaire pour mapper les colonnes booléennes aux noms de partis
partis = {
    'Bord_Centre': 'Centre',
    'Bord_Droite': 'Droite',
    'Bord_Extrêmedroite': 'Extrême Droite',
    'Bord_Extrêmegauche': 'Extrême Gauche',
    'Bord_Gauche': 'Gauche'
}

# Préparer les données
data = []
for annee in df['Annee'].unique():
    for parti in partis:
        # Filtrer les données pour l'année et le parti
        mask = (df['Annee'] == annee) & (df[parti] == True)
        if mask.any():
            row = df[mask].iloc[0]
            data.append({
                'Annee': annee,
                'Parti': partis[parti],
                'Voix_exprimees': row['Ratio_voix_exprime_adjusted']
            })

# Créer un DataFrame à partir des données préparées
df_plot = pd.DataFrame(data)

# Pivoter les données pour avoir les partis en colonnes
pivot_df = df_plot.pivot(index='Annee', columns='Parti', values='Voix_exprimees')

# Créer le graphique
plt.figure(figsize=(12, 7))
ax = pivot_df.plot(kind='bar', stacked=False, width=0.8)

# Personnalisation du graphique
plt.title('Voix exprimées par parti politique et par année', fontsize=14)
plt.xlabel('Année', fontsize=12)
plt.ylabel('Pourcentage de voix exprimées (ajusté)', fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Ajouter les valeurs sur les barres
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}%", 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, 5), 
                textcoords='offset points')

plt.legend(title='Parti politique', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()