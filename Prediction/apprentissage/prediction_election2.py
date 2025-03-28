import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Charger les données
df = pd.read_csv('./Prediction/data/donnees_preparees.csv')

# Filtrer les données pour le tour 1
df_tour1 = df[df['Tour'] == 2]

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