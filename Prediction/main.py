from base.connexion import get_connection
from base.recup_donnees import load_full_data
from preparation.preparation import preparation


# Fonction principale
if __name__ == "__main__":
    # Partie pour récupérer les données
    #load_full_data()

    #Partie pour préparer les données
    preparation()
