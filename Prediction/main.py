from base.connexion import get_connection
from base.recup_donnees import load_full_data
from preparation.preparation import preparation
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import apprentissage.modele1
import apprentissage.modele2
import apprentissage.modele3
import apprentissage.tour2modele1
import apprentissage.tour2modele2
import apprentissage.tour2modele3
import visualisation.visual as visual


# Fonction principale
if __name__ == "__main__":
    # Partie pour récupérer les données
    #load_full_data()

    #Partie pour préparer les données
    #preparation()

    # Appel aux modèles d'apprentissage du premier tour
    models = {
        "Random_Forest": apprentissage.modele1.train_and_evaluate(),
        "Gradient_Boosting": apprentissage.modele2.train_and_evaluate(),
        "XGBoost": apprentissage.modele3.train_and_evaluate(),
    }

    visual.voirmodel(models)

    best_model_name = max(models, key=lambda name: models[name][2]['r2'])
    #model, scaler, scores = models[best_model_name]
    model, scaler, scores = models["Random_Forest"]

    # Prédiction pour 2026–2028
    df_pred = pd.read_csv('./Prediction/data/predictions_2025_2027.csv')
    X_pred = df_pred
    X_pred_scaled = scaler.transform(X_pred)
    y_pred_2025_2027 = model.predict(X_pred_scaled)

    df_pred_predictions = pd.DataFrame(
        y_pred_2025_2027,
        columns=['Pourcentage_Abstention', 'Pourcentage_Votants', 'Ratio_voix_exprime']
    )

    df_pred = pd.concat([df_pred, df_pred_predictions], axis=1)
    df_pred.to_csv('./Prediction/data/predictions_2025_2027_with_predictions.csv', index=False)

    print("Prédictions sauvegardées.")

    # Ajustement
    df_pred = pd.read_csv('./Prediction/data/predictions_2025_2027_with_predictions.csv')

    sum_by_annee = df_pred.groupby('Annee')['Ratio_voix_exprime'].sum()
    df_pred['Ratio_voix_exprime_adjusted'] = df_pred.apply(
        lambda row: row['Ratio_voix_exprime'] * (100 / sum_by_annee[row['Annee']])
        if sum_by_annee[row['Annee']] != 0 else 0,
        axis=1
    )
    df_pred.to_csv('./Prediction/data/predictions_2025_2027_with_predictions_adjusted.csv', index=False)


    # visualisation des résultats tour 1 
    visual.voirtour1()


    # Appel aux modèles d'apprentissage du second tour
    models2 = {
        "Random_Forest": apprentissage.tour2modele1.train_and_evaluate(),
        "Gradient_Boosting": apprentissage.tour2modele2.train_and_evaluate(),
        "XGBoost": apprentissage.tour2modele3.train_and_evaluate(),
    }

    visual.voirmodel(models2)

    best_model_name2 = max(models2, key=lambda name: models2[name][2]['r2'])
    #model2, scaler2, scores2 = models2[best_model_name2]
    model2, scaler2, scores2 = models2["Random_Forest"]


    # filtrage et tri des données
    df = pd.read_csv('./Prediction/data/predictions_2025_2027_with_predictions_adjusted.csv')
    df_sorted = df.sort_values(['Annee', 'Ratio_voix_exprime_adjusted'], ascending=[True, False])

    # Récupration et duplication des 2 premiers candidats par année
    def extraire_et_dupliquer(group):
        top_2 = group.head(2).copy()
        top_2['Tour'] = 2
        return top_2

    df_duplique = df_sorted.groupby('Annee', group_keys=False).apply(extraire_et_dupliquer)
    df_duplique = df_duplique.drop(columns=['Pourcentage_Abstention','Pourcentage_Votants', 'Ratio_voix_exprime', 'Ratio_voix_exprime_adjusted'])
    df_duplique.to_csv('./Prediction/data/predictions_2025_2027_top_2_duplicated.csv', index=False)

    # chargement filtrage et normallisation des données
    df_pred = pd.read_csv('./Prediction/data/predictions_2025_2027_top_2_duplicated.csv')
    X_pred = df_pred
    X_pred_scaled = scaler2.transform(X_pred)

    # prediction pour 2025-2027
    y_pred_2025_2027 = model2.predict(X_pred_scaled)
    df_pred_predictions = pd.DataFrame(y_pred_2025_2027, columns=['Pourcentage_Abstention', 'Pourcentage_Votants', 'Ratio_voix_exprime'])

    # Ajouter les prédictions au DataFrame original si vous souhaitez sauvegarder le fichier complet
    df_pred = pd.concat([df_pred, df_pred_predictions], axis=1)

    # Calculer la somme des valeurs de 'Ratio_voix_exprime' par année
    sum_by_annee = df_pred.groupby('Annee')['Ratio_voix_exprime'].sum()

    # Ajuster les valeurs de 'Ratio_voix_exprime' pour chaque année en utilisant un produit en croix
    df_pred['Ratio_voix_exprime_adjusted'] = df_pred.apply(
        lambda row: row['Ratio_voix_exprime'] * (100 / sum_by_annee[row['Annee']]) 
        if sum_by_annee[row['Annee']] != 0 else 0, axis=1)

    # Enregistrer le dataframe ajusté dans un nouveau fichier CSV
    df_pred.to_csv('./Prediction/data/predictions_2025_2027_top_2_with_predictions_adjusted.csv', index=False)

    # Visualisation des résultats du second tour
    visual.voirtour2()