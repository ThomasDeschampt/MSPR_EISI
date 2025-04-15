import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

def train_and_evaluate():
    df = pd.read_csv('./Prediction/data/donnees_preparees.csv')

    # on filtre le tour 1
    df_tour1 = df[df['Tour'] == 1]

    # Variables d'entrée et de sortie
    X = df_tour1.drop(columns=['Pourcentage_Abstention', 'Pourcentage_Votants', 'Ratio_voix_exprime'])
    y = df_tour1[['Pourcentage_Abstention', 'Pourcentage_Votants', 'Ratio_voix_exprime']]

    # on separe les données en entraînement et test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # standardisation
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Gradient Boosting
    model = MultiOutputRegressor(GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42))
    model.fit(X_train_scaled, y_train)

    # Prédictions test
    y_pred = model.predict(X_test_scaled)

    scores = {
        "mae": mean_absolute_error(y_test, y_pred),
        "mse": mean_squared_error(y_test, y_pred),
        "r2": r2_score(y_test, y_pred)
    }

    return model, scaler, scores