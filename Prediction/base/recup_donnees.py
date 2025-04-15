import pandas as pd
from base.connexion import get_connection

# On récupère les données fusionnées depuis la table de faits et les tables de dimensions
def load_full_data():
    query = """
    SELECT 
        f.Id_fait_election, f.Annee, f.Tour, f.Inscrits, f.Absentions, f.Pourcentage_Abstention, f.Votants, f.Pourcentage_Votants, f.BlancsNuls, f.Nombre_de_voix, f.Ratio_voix_exprime,
        d1.*, d2.*, d3.*, d4.*, d5.*, d6.*, d7.*
    FROM Faits_Elections f
    LEFT JOIN Candidat d1 ON f.Id_candidat = d1.Id_candidat
    LEFT JOIN ConsoMenage d2 ON f.Id_conso_menage = d2.Id_conso_menage
    LEFT JOIN Emplois d3 ON f.Id_emploi = d3.Id_emploi
    LEFT JOIN Insecurite d4 ON f.Id_insecurite = d4.Id_insecurite
    LEFT JOIN Economie d5 ON f.Id_economie = d5.Id_economie
    LEFT JOIN Retraite d6 ON f.Id_retraite = d6.Id_retraite
    LEFT JOIN Demographie d7 ON f.Id_demographie = d7.Id_demographie;
    """

    # On recupère la connexion
    conn = get_connection()
    if conn:
        # On charge les données dans un DataFrame
        df = pd.read_sql(query, conn)
        conn.close()
        print("Données fusionnées :", df.shape)

        # On retire les colonnes inutiles
        df = df.loc[:, ~df.columns.duplicated(keep="first")]
        df.drop(['Id_fait_election', 'Id_demographie', 'Id_conso_menage', 'Id_emploi', 'Id_insecurite', 'Id_economie', 'Id_retraite', 'Id_candidat'], axis=1, inplace=True)
        df.drop(['Inscrits', 'Absentions', 'Votants', 'Nombre_de_voix', 'BlancsNuls'], axis=1, inplace=True)

        # On sauvegarde les données dans un fichier CSV
        df.to_csv('./Prediction/data/donnees_fusionnees.csv', index=False)
        print("Les données ont été sauvegardées dans 'donnees_fusionnees.csv'.")
        
        return df
    else:
        print("Impossible de charger les données.")
        return None
