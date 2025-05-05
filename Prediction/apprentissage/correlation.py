import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Charger les données
df = pd.read_csv('./Prediction/data/donnees_preparees.csv')

# Supprimer les colonnes qui commencent par "Bord"
df_filtered = df.loc[:, ~df.columns.str.startswith('Bord')]

# Calculer la matrice de corrélation
correlation_matrix = df_filtered.corr(numeric_only=True)

# Extraire et trier les corrélations avec 'Ratio_voix_exprime'
target_corr = correlation_matrix[['Ratio_voix_exprime']].sort_values(by='Ratio_voix_exprime', ascending=False)

# Afficher la heatmap
plt.figure(figsize=(8, len(target_corr) * 0.5))
sns.heatmap(target_corr, annot=True, cmap='coolwarm', center=0)
plt.title("Corrélation avec 'Ratio_voix_exprime' (sans les colonnes 'Bord*')")
plt.tight_layout()

# Enregistrer l'image en PNG
plt.savefig("correlation_ratio_voix_exprime.png", dpi=300)

# Afficher le graphique
plt.show()
