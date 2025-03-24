import os 
from valeurs_mensuelles import nettoyer_valeurs_annuelles
from chomage import nettoyer_chomage
from demographie import nettoyer_demographie
from depart_retraite import nettoyer_retraite
from emplois_prive import nettoyer_emplois_prive
from emplois_public import nettoyer_emplois_public
from insecurite import nettoyer_insecurite
from masse_salariale import nettoyer_masse_salariale
from pib import nettoyer_pib
from conso_menage_data import nettoyer_conso_menage_data
from election import nettoyer_election
from candidats import nettoyer_candidats


dossier_entree = "Nettoyage/datasets_origine"
dossier_sortie = "Nettoyage/datasets_nettoyer"

if not os.path.exists(dossier_sortie):
    os.makedirs(dossier_sortie)

fichiers_a_traiter = {
    "chomage.csv": nettoyer_chomage,
    "demographie.csv": nettoyer_demographie,
    "retraite.csv":  nettoyer_retraite,
    "emplois_prive.csv": nettoyer_emplois_prive,
    "emplois_public.csv": nettoyer_emplois_public,
    "insecurite.csv": nettoyer_insecurite,
    "masse_salariale.csv": nettoyer_masse_salariale,
    "pib.csv": nettoyer_pib,
    "conso_menage_data.csv": nettoyer_conso_menage_data,
    "elections.csv": nettoyer_election,
    "candidats.csv": nettoyer_candidats,
    "valeurs_mensuelles.csv" : nettoyer_valeurs_annuelles
}

for fichier, fonction in fichiers_a_traiter.items():
    chemin_fichier = os.path.join(dossier_entree,fichier)
    if os.path.exists(chemin_fichier):
        print(f"Traitement du fichier {fichier}")
        fonction(chemin_fichier, dossier_sortie)
    else :
        print(f"Le fichier {fichier} n'existe pas")

print("le singe est mort , les baloons passes")