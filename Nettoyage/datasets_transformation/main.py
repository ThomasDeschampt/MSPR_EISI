import os 
from chomage import nettoyer_chomage
from commiseriat import nettoyer_commiseriat
from conso_menage_data import nettoyer_conso_menage_data
from demographie import nettoyer_demographie
from depart_retraite import nettoyer_depart_retraite
from emplois_prive import nettoyer_emplois_prive
from emplois_public import nettoyer_emplois_public
from insecurite import nettoyer_insecurite
from masse_salariale import nettoyer_masse_salariale
from pib import nettoyer_pib


dossier_entree = "Nettoyage/datasets_origine"
dossier_sortie = "Nettoyage/datasets_nettoyer"

if not os.path.exists(dossier_sortie):
    os.makedirs(dossier_sortie)

fichiers_a_traiter = {
    "chomage.csv": nettoyer_chomage,
    "commiseriat.csv": nettoyer_commiseriat,
    "conso_menage_data.csv": nettoyer_conso_menage_data,
    "demographie.csv": nettoyer_demographie,
    "depart_retraite.csv":  nettoyer_depart_retraite,
    "emplois_prive.csv": nettoyer_emplois_prive,
    "emplois_public.csv": nettoyer_emplois_public,
    "insecurite.csv": nettoyer_insecurite,
    "masse_salariale.csv": nettoyer_masse_salariale,
    "pib.csv": nettoyer_pib,

    
}

for fichier, fonction in fichiers_a_traiter.items():
    chemin_fichier = os.path.join(dossier_entree,fichier)
    if os.path.exists(chemin_fichier):
        print(f"Traitement du fichier {fichier}")
        fonction(chemin_fichier, dossier_sortie)
    else :
        print(f"Le fichier {fichier} n'existe pas")

print("le singe est mort , les baloons passes")