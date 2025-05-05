from base.connexion import get_connection
from base.recup_donnees import load_full_data
from preparation.preparation import preparation
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import logging
import os
from datetime import datetime
import apprentissage.modele1
import apprentissage.modele2
import apprentissage.modele3
import apprentissage.tour2modele1
import apprentissage.tour2modele2
import apprentissage.tour2modele3
import visualisation.visual as visual


# Configuration du logger
def setup_logger(log_dir='./Prediction/logs'):
    """
    Configure un logger pour le projet de prédiction électorale.
    
    Args:
        log_dir (str): Répertoire où seront stockés les logs
        
    Returns:
        logging.Logger: L'objet logger configuré
    """
    # Création du répertoire de logs s'il n'existe pas
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Nom du fichier de log avec timestamp
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"prediction_{current_time}.log")
    
    # Configuration du logger
    logger = logging.getLogger('prediction_electorale')
    logger.setLevel(logging.DEBUG)
    
    # Handler pour fichier
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Handler pour console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Ajout des handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info("Logger initialisé")
    return logger


# Fonction pour afficher les gagnants par année
def print_winners(logger):
    """
    Affiche les gagnants des élections par année basé sur les prédictions
    """
    try:
        # Pour le premier tour
        logger.info("Analyse des résultats du premier tour...")
        df_tour1 = pd.read_csv('./Prediction/data/predictions_2025_2027_with_predictions_adjusted.csv')
        
        # Dictionnaire pour mapper les colonnes booléennes aux noms de partis
        partis = {
            'Bord_Centre': 'Centre',
            'Bord_Droite': 'Droite',
            'Bord_Extrêmedroite': 'Extrême Droite',
            'Bord_Extrêmegauche': 'Extrême Gauche',
            'Bord_Gauche': 'Gauche'
        }
        
        # Affichage des deux premiers par année pour le premier tour
        print("\n===== RÉSULTATS DU PREMIER TOUR =====")
        for annee in sorted(df_tour1['Annee'].unique()):
            if annee == 2025:  # On ignore 2025 si nécessaire
                continue
                
            df_annee = df_tour1[df_tour1['Annee'] == annee].copy()
            df_annee = df_annee.sort_values('Ratio_voix_exprime_adjusted', ascending=False)
            
            print(f"\nAnnée {annee} - Premier tour:")
            for i, (_, row) in enumerate(df_annee.head(2).iterrows()):
                # Déterminer le parti
                parti = None
                for bord, nom in partis.items():
                    if row[bord]:
                        parti = nom
                        break
                
                position = "1er" if i == 0 else "2ème"
                score = row['Ratio_voix_exprime_adjusted']
                print(f"  {position}: {parti} - {score:.2f}%")
        
        # Pour le second tour
        logger.info("Analyse des résultats du second tour...")
        try:
            df_tour2 = pd.read_csv('./Prediction/data/predictions_2025_2027_top_2_with_predictions_adjusted.csv')
            
            print("\n===== RÉSULTATS DU SECOND TOUR =====")
            for annee in sorted(df_tour2['Annee'].unique()):
                if annee == 2025:  # On ignore 2025 si nécessaire
                    continue
                    
                df_annee = df_tour2[df_tour2['Annee'] == annee].copy()
                df_annee = df_annee.sort_values('Ratio_voix_exprime_adjusted', ascending=False)
                
                # Déterminer le gagnant
                if len(df_annee) > 0:
                    row_gagnant = df_annee.iloc[0]
                    
                    # Déterminer le parti
                    parti_gagnant = None
                    for bord, nom in partis.items():
                        if row_gagnant[bord]:
                            parti_gagnant = nom
                            break
                    
                    score_gagnant = row_gagnant['Ratio_voix_exprime_adjusted']
                    
                    # Afficher le résultat
                    print(f"\nAnnée {annee} - GAGNANT: {parti_gagnant} avec {score_gagnant:.2f}%")
                    
                    # Si on a un deuxième candidat
                    if len(df_annee) > 1:
                        row_second = df_annee.iloc[1]
                        parti_second = None
                        for bord, nom in partis.items():
                            if row_second[bord]:
                                parti_second = nom
                                break
                        
                        score_second = row_second['Ratio_voix_exprime_adjusted']
                        print(f"  2ème: {parti_second} avec {score_second:.2f}%")
                        print(f"  Écart: {score_gagnant - score_second:.2f} points")
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse des résultats du second tour: {str(e)}")
            print("\nImpossible d'afficher les résultats du second tour. Consultez les logs pour plus de détails.")
            
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage des gagnants: {str(e)}")
        print("\nImpossible d'afficher les résultats. Consultez les logs pour plus de détails.")


# Fonction principale
if __name__ == "__main__":
    # Configuration du logger
    logger = setup_logger()
    logger.info("Démarrage du programme de prédiction électorale")
    
    # Partie pour récupérer les données
    # logger.info("Chargement des données...")
    # try:
    #     load_full_data()
    #     logger.info("Données chargées avec succès")
    # except Exception as e:
    #     logger.error(f"Erreur lors du chargement des données: {str(e)}")
    #     logger.info("Utilisation des données existantes")

    # Partie pour préparer les données
    logger.info("Préparation des données...")
    try:
        preparation()
        logger.info("Données préparées avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de la préparation des données: {str(e)}")
        logger.info("Utilisation des données préparées existantes")

    # Appel aux modèles d'apprentissage du premier tour
    logger.info("Entraînement des modèles pour le premier tour...")
    models = {}
    
    try:
        models["Random_Forest"] = apprentissage.modele1.train_and_evaluate()
        logger.info("Modèle Random Forest entraîné avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement du modèle Random Forest: {str(e)}")
    
    try:
        models["Gradient_Boosting"] = apprentissage.modele2.train_and_evaluate()
        logger.info("Modèle Gradient Boosting entraîné avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement du modèle Gradient Boosting: {str(e)}")
    
    try:
        models["XGBoost"] = apprentissage.modele3.train_and_evaluate()
        logger.info("Modèle XGBoost entraîné avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement du modèle XGBoost: {str(e)}")
    
    for model_name, (_, _, scores) in models.items():
        logger.info(f"Performances du modèle {model_name} - Premier tour : MAE={scores['mae']:.4f}, MSE={scores['mse']:.4f}, R²={scores['r2']:.4f}")

    logger.info("Affichage des performances des modèles du premier tour")
    try:
        visual.voirmodel(models)
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage des performances des modèles: {str(e)}")

    # Sélection du meilleur modèle
    if models:
        best_model_name = max(models, key=lambda name: models[name][2]['r2'])
        logger.info(f"Meilleur modèle pour le premier tour : {best_model_name} avec R²={models[best_model_name][2]['r2']:.4f}")
        
        #model, scaler, scores = models[best_model_name]
        model, scaler, scores = models["Random_Forest"]
        logger.info(f"Modèle sélectionné pour les prédictions : Random_Forest")

        # Prédiction pour 2025–2028
        logger.info("Chargement des données de prédiction...")
        try:
            df_pred = pd.read_csv('./Prediction/data/predictions_2025_2027.csv')
            logger.info(f"Données chargées : {df_pred.shape[0]} lignes, {df_pred.shape[1]} colonnes")
            
            logger.info("Normalisation des données de prédiction...")
            X_pred = df_pred
            X_pred_scaled = scaler.transform(X_pred)
            
            logger.info("Prédiction des résultats pour 2025-2027...")
            y_pred_2025_2027 = model.predict(X_pred_scaled)

            df_pred_predictions = pd.DataFrame(
                y_pred_2025_2027,
                columns=['Pourcentage_Abstention', 'Pourcentage_Votants', 'Ratio_voix_exprime']
            )

            df_pred = pd.concat([df_pred, df_pred_predictions], axis=1)
            
            try:
                df_pred.to_csv('./Prediction/data/predictions_2025_2027_with_predictions.csv', index=False)
                logger.info("Prédictions sauvegardées dans 'predictions_2025_2027_with_predictions.csv'")
            except Exception as e:
                logger.error(f"Erreur lors de la sauvegarde des prédictions: {str(e)}")

            # Ajustement pour le ratio de voix exprimées
            logger.info("Ajustement des ratios de voix exprimées...")
            try:
                df_pred = pd.read_csv('./Prediction/data/predictions_2025_2027_with_predictions.csv')

                sum_by_annee = df_pred.groupby('Annee')['Ratio_voix_exprime'].sum()
                logger.info(f"Somme des ratios par année avant ajustement: {sum_by_annee.to_dict()}")
                
                df_pred['Ratio_voix_exprime_adjusted'] = df_pred.apply(
                    lambda row: row['Ratio_voix_exprime'] * (100 / sum_by_annee[row['Annee']])
                    if sum_by_annee[row['Annee']] != 0 else 0,
                    axis=1
                )
                
                df_pred.to_csv('./Prediction/data/predictions_2025_2027_with_predictions_adjusted.csv', index=False)
                logger.info("Prédictions ajustées sauvegardées dans 'predictions_2025_2027_with_predictions_adjusted.csv'")
            except Exception as e:
                logger.error(f"Erreur lors de l'ajustement des ratios: {str(e)}")

            # visualisation des résultats tour 1 
            logger.info("Génération des visualisations pour le premier tour...")
            try:
                visual.voirtour1()
                logger.info("Visualisations du premier tour générées avec succès")
            except Exception as e:
                logger.error(f"Erreur lors de la génération des visualisations du premier tour: {str(e)}")
        except Exception as e:
            logger.error(f"Erreur lors des prédictions du premier tour: {str(e)}")
    else:
        logger.error("Aucun modèle n'a été correctement entraîné pour le premier tour")

    # Appel aux modèles d'apprentissage du second tour
    logger.info("Entraînement des modèles pour le second tour...")
    models2 = {}
    
    try:
        models2["Random_Forest"] = apprentissage.tour2modele1.train_and_evaluate()
        logger.info("Modèle Random Forest (tour 2) entraîné avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement du modèle Random Forest (tour 2): {str(e)}")
    
    try:
        models2["Gradient_Boosting"] = apprentissage.tour2modele2.train_and_evaluate()
        logger.info("Modèle Gradient Boosting (tour 2) entraîné avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement du modèle Gradient Boosting (tour 2): {str(e)}")
    
    try:
        models2["XGBoost"] = apprentissage.tour2modele3.train_and_evaluate()
        logger.info("Modèle XGBoost (tour 2) entraîné avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement du modèle XGBoost (tour 2): {str(e)}")
    
    if models2:
        for model_name, (_, _, scores) in models2.items():
            logger.info(f"Performances du modèle {model_name} - Second tour : MAE={scores['mae']:.4f}, MSE={scores['mse']:.4f}, R²={scores['r2']:.4f}")

        logger.info("Affichage des performances des modèles du second tour")
        try:
            visual.voirmodel(models2)
        except Exception as e:
            logger.error(f"Erreur lors de l'affichage des performances des modèles (tour 2): {str(e)}")

        # Sélection du meilleur modèle
        best_model_name2 = max(models2, key=lambda name: models2[name][2]['r2'])
        logger.info(f"Meilleur modèle pour le second tour : {best_model_name2} avec R²={models2[best_model_name2][2]['r2']:.4f}")
        
        #model2, scaler2, scores2 = models2[best_model_name2]
        model2, scaler2, scores2 = models2["Random_Forest"]
        logger.info(f"Modèle sélectionné pour les prédictions du second tour : Random_Forest")

        # filtrage et tri des données
        logger.info("Préparation des données pour les prédictions du second tour...")
        try:
            df = pd.read_csv('./Prediction/data/predictions_2025_2027_with_predictions_adjusted.csv')
            df_sorted = df.sort_values(['Annee', 'Ratio_voix_exprime_adjusted'], ascending=[True, False])
            logger.info(f"Données triées : premiers candidats par année")

            # Récupération et duplication des 2 premiers candidats par année
            logger.info("Extraction des deux premiers candidats par année...")
            def extraire_et_dupliquer(group):
                top_2 = group.head(2).copy()
                top_2['Tour'] = 2
                return top_2

            df_duplique = df_sorted.groupby('Annee', group_keys=False).apply(extraire_et_dupliquer)
            df_duplique = df_duplique.drop(columns=['Pourcentage_Abstention','Pourcentage_Votants', 'Ratio_voix_exprime', 'Ratio_voix_exprime_adjusted'])
            
            try:
                df_duplique.to_csv('./Prediction/data/predictions_2025_2027_top_2_duplicated.csv', index=False)
                logger.info(f"Candidats du second tour extraits : {df_duplique.shape[0]} candidats, sauvegardés dans 'predictions_2025_2027_top_2_duplicated.csv'")
            except Exception as e:
                logger.error(f"Erreur lors de la sauvegarde des candidats du second tour: {str(e)}")

            # chargement filtrage et normalisation des données
            logger.info("Normalisation des données pour le second tour...")
            try:
                df_pred = pd.read_csv('./Prediction/data/predictions_2025_2027_top_2_duplicated.csv')
                X_pred = df_pred
                X_pred_scaled = scaler2.transform(X_pred)

                # prediction pour 2025-2028
                logger.info("Prédiction des résultats du second tour...")
                y_pred_2025_2027 = model2.predict(X_pred_scaled)
                df_pred_predictions = pd.DataFrame(y_pred_2025_2027, columns=['Pourcentage_Abstention', 'Pourcentage_Votants', 'Ratio_voix_exprime'])

                # on ajoute les predictions au dataframe
                df_pred = pd.concat([df_pred, df_pred_predictions], axis=1)

                # on calcule la somme des valeurs de 'Ratio_voix_exprime' par année
                sum_by_annee = df_pred.groupby('Annee')['Ratio_voix_exprime'].sum()
                logger.info(f"Somme des ratios par année (second tour) avant ajustement: {sum_by_annee.to_dict()}")

                # ajustement du ratio de voix exprimées
                logger.info("Ajustement des ratios pour le second tour...")
                df_pred['Ratio_voix_exprime_adjusted'] = df_pred.apply(
                    lambda row: row['Ratio_voix_exprime'] * (100 / sum_by_annee[row['Annee']]) 
                    if sum_by_annee[row['Annee']] != 0 else 0, axis=1)

                try:
                    df_pred.to_csv('./Prediction/data/predictions_2025_2027_top_2_with_predictions_adjusted.csv', index=False)
                    logger.info("Prédictions du second tour sauvegardées dans 'predictions_2025_2027_top_2_with_predictions_adjusted.csv'")
                except Exception as e:
                    logger.error(f"Erreur lors de la sauvegarde des prédictions du second tour: {str(e)}")

                # Visualisation des résultats du second tour
                logger.info("Génération des visualisations pour le second tour...")
                try:
                    visual.voirtour2()
                    logger.info("Visualisations du second tour générées avec succès")
                except Exception as e:
                    logger.error(f"Erreur lors de la génération des visualisations du second tour: {str(e)}")
            except Exception as e:
                logger.error(f"Erreur lors de la prédiction des résultats du second tour: {str(e)}")
        except Exception as e:
            logger.error(f"Erreur lors de la préparation des données pour le second tour: {str(e)}")
    else:
        logger.error("Aucun modèle n'a été correctement entraîné pour le second tour")
    
    # Affichage des gagnants
    logger.info("Affichage des résultats finaux et des gagnants")
    print_winners(logger)
    
    logger.info("Programme terminé")
    print("\nTraitement terminé. Consultez les logs pour plus de détails.")