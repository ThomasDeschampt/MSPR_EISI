import pandas as pd
import random
import re

# on charge le CSV depuis chemin relatif explicite
df = pd.read_csv('./Prediction/data/donnees_fusionnees.csv')

# génération de trigrammes aléatoires
def generer_trigramme_aleatoire():
    lettres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choice(lettres) for _ in range(3))

def generer_trigrammes_aleatoires(nb=10):
    resultat = set()
    while len(resultat) < nb:
        resultat.add(generer_trigramme_aleatoire())
    return list(resultat)

# Génération et affichage
trigrammes_futurs = generer_trigrammes_aleatoires(nb=10)
print("Trigrammes futurs prédits :")
print(trigrammes_futurs)