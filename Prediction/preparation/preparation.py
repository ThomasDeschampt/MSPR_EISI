import pandas as pd
from sklearn.preprocessing import StandardScaler


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


# On traite les valeurs manquantes
pd.set_option('display.max_rows', None)
print(df.isna().sum()[df.isna().sum() > 0])

# A FAIRE
# choisir pour chaque colonne la méthode de traitement des valeurs manquantes (moyenne, médiane, interpolation ou suppression)
# ou trouver les données à la main (certains csv il manque juste quelques années pour une colonne)



# On supprime les colonnes qui n'ont pas de corrélation avec le vote
correlation = df.corr()['Ratio_voix_exprime'].sort_values(ascending=False)

#A FAIRE

