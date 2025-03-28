import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import xgboost as xgb  # XGBoost
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Charger les données à partir du fichier CSV
df = pd.read_csv("Prediction/data/donnees_preparees.csv", sep=",")

# Préparer les variables d'entrée et de sortie
X = df.drop(columns=["Annee", "Bord_Centre", "Bord_Droite", "Bord_Extrêmedroite", 
                     "Bord_Extrêmegauche", "Bord_Gauche"])  # Supprimer les colonnes inutiles
y = df[["Bord_Centre", "Bord_Droite", "Bord_Extrêmedroite", "Bord_Extrêmegauche", "Bord_Gauche"]].idxmax(axis=1)

# Encoder la variable cible
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# Standardiser les variables numériques
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Séparer en train/test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Entraîner le modèle XGBoost
model = xgb.XGBClassifier(random_state=42)
model.fit(X_train, y_train)

# Prédictions et évaluation
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Passer les prédictions et les valeurs réelles à classification_report
print(classification_report(y_test, y_pred))

# Sauvegarder le modèle
joblib.dump(model, "modele_elections_xgboost.pkl")

print("Modèle de prédiction des élections (XGBoost) entraîné et sauvegardé avec succès")
