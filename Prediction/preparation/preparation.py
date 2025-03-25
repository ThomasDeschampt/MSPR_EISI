import pandas as pd
from sklearn.preprocessing import StandardScaler

def preparation():
    # On recupere le csv contenant les données fusionnées
    df = pd.read_csv('./Prediction/data/donnees_fusionnees.csv')

    # On verifie les types de colonnes
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns

    # On encode les colonnes catégorielles
    df = pd.get_dummies(df, columns=categorical_columns)

    # On normalise les données
    scaler = StandardScaler()
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

    # On supprime les années sans election
    df = df.dropna(subset=['Tour'])