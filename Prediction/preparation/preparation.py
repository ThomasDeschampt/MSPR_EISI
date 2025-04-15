import pandas as pd
from sklearn.preprocessing import StandardScaler

def preparation():
    # On recupere le csv
    df = pd.read_csv('./Prediction/data/donnees_fusionnees.csv')

    # On verifie les types de colonnes
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns

    # On encode les colonnes catégorielles
    df = pd.get_dummies(df, columns=categorical_columns)

    # On fait un lissage sur la colonne Ratio_voix_exprime en groupant par Tour et Annee
    df['Ratio_voix_exprime'] = df.groupby(['Tour', 'Annee'])['Ratio_voix_exprime'].transform(lambda x: x.rolling(window=3, min_periods=1, center=True).mean().round(2))

    # On supprime les années sans election
    df = df.dropna(subset=['Tour'])

    # On supprime les colonnes qui commence par 'Parti'
    df = df[df.columns.drop(list(df.filter(regex='Parti')))]

    # on affiche de la corrélation avec la colonne Ratio_voix_exprime dans l'ordre décroissant
    pd.set_option('display.max_rows', None)
    print(df.corr()['Ratio_voix_exprime'].sort_values(ascending=False))

    # On sauvegarde les données préparées
    df.to_csv('./Prediction/data/donnees_preparees.csv', index=False)
