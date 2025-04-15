import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def voirtour1 ():
    df = pd.read_csv('./Prediction/data/predictions_2025_2027_with_predictions_adjusted.csv')

    # Dictionnaire pour mapper les colonnes booléennes aux noms de partis
    partis = {
        'Bord_Centre': 'Centre',
        'Bord_Droite': 'Droite',
        'Bord_Extrêmedroite': 'Extrême Droite',
        'Bord_Extrêmegauche': 'Extrême Gauche',
        'Bord_Gauche': 'Gauche'
    }

    # on prépare les données
    data = []
    for annee in df['Annee'].unique():
        if annee == 2025:
            continue
        
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
    # couleur en fonction du parti
    colors = {
        'Droite': '#000066',            
        'Extrême Droite': '#2A3CB0',    
        'Gauche': '#B0B0B0',           
        'Extrême Gauche': '#888888',    
        'Centre': '#E1000F'           
    }

    # On met en mode colonne
    pivot_df = df_plot.pivot(index='Annee', columns='Parti', values='Voix_exprimees')

    # creation du graphique
    plt.figure(figsize=(12, 7))
    ax = pivot_df.plot(kind='bar', stacked=False, width=0.8, color=[colors[col] for col in pivot_df.columns])

    # personnalisation du graphique
    plt.title('Voix exprimées par parti politique et par année', fontsize=14)
    plt.xlabel('Année', fontsize=12)
    plt.ylabel('Pourcentage de voix exprimées (ajusté)', fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # on ajoute les valeurs sur les barres
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 5), 
                    textcoords='offset points')

    plt.legend(title='Parti politique', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


def voirtour2 ():
    df = pd.read_csv('./Prediction/data/predictions_2025_2027_top_2_with_predictions_adjusted.csv')

    # Dictionnaire pour mapper les colonnes booléennes aux noms de partis
    partis = {
        'Bord_Centre': 'Centre',
        'Bord_Droite': 'Droite',
        'Bord_Extrêmedroite': 'Extrême Droite',
        'Bord_Extrêmegauche': 'Extrême Gauche',
        'Bord_Gauche': 'Gauche'
    }

    # on prepare les données
    data = []
    for annee in df['Annee'].unique():
        if annee == 2025:
            continue

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

    # on met en mode colonne
    pivot_df = df_plot.pivot(index='Annee', columns='Parti', values='Voix_exprimees')

    # creation du graphique
    plt.figure(figsize=(12, 7))
    # couleur en fonction du parti
    colors = {
        'Droite': '#000091',
        'Extrême Droite': '#000091',
        'Gauche': '#ffffff',
        'Extrême Gauche': '#ffffff',
        'Centre': '#E1000f'
    }
    ax = pivot_df.plot(kind='bar', stacked=False, width=0.8, color=[colors[col] for col in pivot_df.columns])


    # on personnalise le graphique
    plt.title('Voix exprimées par parti politique et par année', fontsize=14)
    plt.xlabel('Année', fontsize=12)
    plt.ylabel('Pourcentage de voix exprimées', fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # on ajoute les valeurs sur les barres
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 5), 
                    textcoords='offset points')

    plt.legend(title='Parti politique', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def voirmodel(models):
    # on extrait les scores pour chaque modèle
    maes = {name: model_data[2]['mae'] for name, model_data in models.items()}
    mses = {name: model_data[2]['mse'] for name, model_data in models.items()}
    r2s  = {name: model_data[2]['r2']  for name, model_data in models.items()}

    labels = list(models.keys())
    x = range(len(labels))

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    colors = {
        'MAE': '#000091',
        'MSE': '#ffffff',
        'R²': '#E1000f'
    }

    # fonction pour tracer les barres
    def plot_metric(ax, data, title, color, ylabel):
        values = [data[label] for label in labels]
        ax.bar(x, values, color=color, edgecolor='black')
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylabel(ylabel)
        ax.grid(axis='y', linestyle='--', alpha=0.6)

        # on affiche les valeurs sur les barres
        for i, v in enumerate(values):
            ax.text(i, v, f"{v:.3f}", ha='center', va='bottom', fontsize=9)

        # on ajuste les limites de l'axe y
        # pour éviter que les barres soient trop proches du haut du graphique
        min_val = min(values)
        max_val = max(values)
        margin = (max_val - min_val) * 0.2 if max_val != min_val else 0.1
        ax.set_ylim([min_val - margin, max_val + margin])

    plot_metric(axs[0], maes, 'MAE', colors['MAE'], 'Erreur absolue moyenne')
    plot_metric(axs[1], mses, 'MSE', colors['MSE'], 'Erreur quadratique moyenne')
    plot_metric(axs[2], r2s,  'R² Score', colors['R²'], 'Score de détermination')

    plt.suptitle("Comparaison des performances des modèles", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
