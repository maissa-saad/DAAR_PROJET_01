# ============================================================
# Test de conformite : myegrep doit donner EXACTEMENT
# le meme resultat que egrep (grep -E) sur chaque motif.
# Prerequis : avoir lance "make" (pour creer ./myegrep)
# ============================================================

import os
import subprocess
import pytest

FICHIERS = ["tests/data/petit.txt", "tests/data/56667-0.txt"]

MOTIFS = [
    "Sargon",            # mot simple
    "S(a|g|r)+on",       # exemple de l'enonce
    "Babylon|Assyria",   # alternative
    "(K|k)ing",          # parentheses + alternative
    "Eu.hrates",         # point
    "a.c",               # point entre deux lettres
    "(ab)*c",            # etoile sur un groupe
    "ab*c",              # etoile sur une lettre
    "Th(e|is) ",         # avec un espace
    "a*",                # accepte le mot vide : toutes les lignes
    "xyzxyz",            # introuvable : code de retour 1
]


def lancer(commande):
    """Lance une commande et renvoie (texte affiche, code de retour)."""
    resultat = subprocess.run(commande, capture_output=True)
    return resultat.stdout, resultat.returncode


def test_conformite_avec_egrep():
    if not os.path.exists("./myegrep"):
        pytest.skip("lancer 'make' avant ce test")

    for fichier in FICHIERS:
        if not os.path.exists(fichier):
            print("fichier absent, ignore :", fichier, "(lancer tests/download.sh)")
            continue
        for motif in MOTIFS:
            mon = lancer(["./myegrep", motif, fichier])
            vrai = lancer(["grep", "-E", motif, fichier])
            assert mon == vrai, "difference pour le motif " + motif + " sur " + fichier